import os
import json
import string
import functools
from typing import Dict

from PIL import Image, ImageDraw, ImageFont

from ..common import PRIVATE_DATA_PATH
from .. import common_draw

BANK_BRANCHES_CACHE = {}


@functools.lru_cache()
def get_name_translations():
    with open(os.path.join(PRIVATE_DATA_PATH, 'name_translations.json')) as f:
        return json.load(f)


def _(text):
    return get_name_translations()[text]


class BankStatement:

    def __init__(self, bank, test=False, no_bg=False, mock=False, no_pdf=False, source_image=None, **kwargs):
        self.provider = bank.provider
        self.bank = bank
        self.test = test
        self.no_bg = no_bg
        self.mock = mock
        self.no_pdf = no_pdf
        self.source_image = source_image

    def save_init(self, output_path, source_file_name, annotation_labels_item_filter, labels):
        original_width, original_height, res_labels = common_draw.init_draw_labels(
            annotation_labels_item_filter, 'label_studio_bank_statements.json', 'min',
            labels, mock=self.mock
        )
        image_draw, image = common_draw.init_draw_image(
            output_path, source_file_name, original_width, original_height, getattr(self, 'source_image', None)
        )
        return image_draw, res_labels, image

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

    def draw_textbox(self, *args, **kwargs):
        return common_draw.draw_textbox(*args, no_bg=self.no_bg, **kwargs)

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
