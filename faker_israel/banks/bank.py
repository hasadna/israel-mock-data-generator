import os
import json
import string
from typing import Dict

from PIL import Image, ImageDraw, ImageFont

from ..common import PRIVATE_DATA_PATH

BANK_BRANCHES_CACHE = {}


class BankStatement:

    def __init__(self, bank, test=False, no_bg=False, mock=False, no_pdf=False, source_image=None, **kwargs):
        self.provider = bank.provider
        self.bank = bank
        self.test = test
        self.no_bg = no_bg
        self.mock = mock
        self.no_pdf = no_pdf
        self.source_image = source_image

    def get_annotation_labels(self, item_filter):
        with open(os.path.join(PRIVATE_DATA_PATH, 'label_studio_bank_statements.json'), encoding='utf-8') as f:
            items = [item for item in json.load(f) if item_filter(item)]
            assert len(items) == 1
        item = items[0]
        original_width, original_height = None, None
        res = {}
        for label in item['label']:
            if not original_width:
                original_width = label['original_width']
            else:
                assert original_width == label['original_width']
            if not original_height:
                original_height = label['original_height']
            else:
                assert original_height == label['original_height']
            x = label['x'] * original_width / 100
            y = label['y'] * original_height / 100
            width = label['width'] * original_width / 100
            height = label['height'] * original_height / 100
            assert label['rotation'] == 0
            assert len(label['rectanglelabels']) == 1
            assert label['rectanglelabels'][0] not in res
            res[label['rectanglelabels'][0]] = {
                'x': x,
                'y': y,
                'width': width,
                'height': height,
            }
        return original_width, original_height, res

    def get_draw_labels(self, annotation_labels_item_filter, labels):
        original_width, original_height, annotation_labels = self.get_annotation_labels(annotation_labels_item_filter)
        res_labels = {}
        for label_id, label in labels.items():
            label = {**annotation_labels[label_id], **label}
            label['font_path'] = os.path.join(PRIVATE_DATA_PATH, 'fonts', f'{label["font"]}.ttf')
            if self.mock:
                label['text'] = 'ללקקףףזזץץ'
            res_labels[label_id] = label
        return original_width, original_height, res_labels

    def save_init(self, output_path, source_file_name, annotation_labels_item_filter, labels):
        assert output_path.endswith('.png')
        original_width, original_height, draw_labels = self.get_draw_labels(annotation_labels_item_filter, labels)
        source_image = getattr(self, 'source_image', None)
        if not source_image:
            source_image = os.path.join(PRIVATE_DATA_PATH, f'{source_file_name}.png')
        image = Image.open(source_image)
        assert original_width == image.width
        assert original_height == image.height
        return ImageDraw.Draw(image), draw_labels, image

    def save_save(self, output_path, image, pdf_output_path=None, **kwargs):
        assert output_path.endswith('.png')
        resized_image = image.resize((image.width // 2, image.height // 2))
        resized_image.save(output_path)
        if not self.no_pdf:
            if pdf_output_path:
                assert pdf_output_path.endswith('.pdf')
            else:
                pdf_output_path = output_path.replace('.png', '.pdf')
            resized_image.convert('RGB').save(pdf_output_path)

    def draw_textbox(self, draw, font_path=None, font_size=None, text=None,
                     color=None, direction='rtl', font=None, offset_y=None,
                     x=None, y=None, width=None, height=None,
                     x_offset=None, y_offset=None, center=None,
                     **kwargs):
        if not font or isinstance(font, str):
            font = ImageFont.truetype(font_path, font_size)
        left, top, right, bottom = font.getbbox(text, direction=direction)
        bg_pos_rect = (x, y, x + width, y + height)
        if center:
            text_pos_xy = (
                x + (width - right + left) / 2 + (x_offset or 0),
                y + (height - bottom + top) / 2 + (y_offset or 0),
            )
        else:
            text_pos_xy = (
                x + width - right + (x_offset or 0),
                y + (y_offset or 0)
            )
        if not self.no_bg and bg_pos_rect:
            if offset_y:
                bg_pos_rect = (bg_pos_rect[0], bg_pos_rect[1] + offset_y, bg_pos_rect[2], bg_pos_rect[3] + offset_y)
            draw.rectangle(bg_pos_rect, fill="white")
        if offset_y:
            text_pos_xy = (text_pos_xy[0], text_pos_xy[1] + offset_y)
        draw.text(text_pos_xy, text, fill=color or (0, 0, 0), font=font, direction=direction)
        return font

    def copy_section(self, image, draw, top_y, bottom_y, offset_y, fill=None):
        section = image.crop((0, top_y, image.width, bottom_y))
        image.paste(section, (0, int(top_y + offset_y)))
        if fill:
            draw.rectangle((0, top_y, image.width, top_y + offset_y), fill=fill)


class BankBranch:

    def __init__(self, bank, name, number, phone_number=None, address=None, manager_name=None, manager_phone_number=None,
                 address_city=None, faker_var_value_bank_branch_is_valid_fields=None):
        self.bank = bank
        self.name = name
        self.number = number
        self.phone_number = phone_number if phone_number else self.bank.provider.generator.phone_number()
        if address:
            assert not address_city
            self.address = address
        elif address_city:
            self.address = f'{self.bank.provider.generator.street_address()}, {address_city}'
        else:
            self.address = self.bank.provider.generator.address()
        self.manager_name = manager_name if manager_name else self.bank.provider.generator.name()
        self.manager_phone_number = manager_phone_number if manager_phone_number else self.bank.provider.generator.phone_number()
        self.faker_var_value_bank_branch_is_valid_fields = faker_var_value_bank_branch_is_valid_fields or [
            'name', 'number', 'address', 'phone_number'
        ]

    def iban(self, bank_account_number=None):
        return self.bank.iban()

    def __str__(self):
        return json.dumps(self.as_dict())

    def as_dict(self):
        return {
            'bank_name': self.bank.name,
            'number': self.number,
            'name': self.name,
            'address': self.address,
            'phone_number': self.phone_number,
            'manager_name': self.manager_name,
            'manager_phone_number': self.manager_phone_number,
        }

    def faker_var_value_is_valid(self, faker_var_value):
        for attr in self.faker_var_value_bank_branch_is_valid_fields:
            val = getattr(self, attr)
            if val and not faker_var_value.is_valid(str(val)):
                return False
        return True


class Bank:
    ALPHA: Dict[str, str] = {c: str(ord(c) % 55) for c in string.ascii_uppercase}

    def __init__(self, id_, provider):
        self.id = id_
        self.provider = provider

    def branch(self, **kwargs):
        if self.id not in BANK_BRANCHES_CACHE:
            BANK_BRANCHES_CACHE[self.id] = list(self.iterate_all_branches(**kwargs))
        return self.provider.random_element(BANK_BRANCHES_CACHE[self.id])

    def account_number(self):
        return self.provider.numerify('#########')

    def iban(self, bank_account_number=None):
        bban = self.provider.generator.bban()
        check = bban + "IL00"
        check_ = int("".join(self.ALPHA.get(c, c) for c in check))
        check_ = 98 - (check_ % 97)
        check = str(check_).zfill(2)
        return 'IL' + check + bban

    def iterate_all_branches(self, **kwargs):
        raise NotImplementedError()

    def statement(self, **kwargs):
        raise NotImplementedError()
