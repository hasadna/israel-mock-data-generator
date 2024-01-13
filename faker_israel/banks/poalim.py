import os
import json
from collections import OrderedDict

from .bank import Bank, BankBranch, BankStatement


class BankStatementPoalim(BankStatement):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        fake = self.provider.generator
        related_names = fake.related_names()
        full_name = related_names.name()
        account_number = self.bank.account_number()
        branch = self.bank.branch()
        num_extra_names = fake.random_int(0, 4)
        self.extra_names = []
        for i in range(num_extra_names):
            self.extra_names.append((
                related_names.name(),
                fake.teudat_zehut()
            ))
        num_meyupe = fake.random_element(OrderedDict([
            (0, 0.7),
            (1, 0.2),
            (2, 0.1),
            (3, 0.05),
        ]))
        self.meyupe = []
        for i in range(num_meyupe):
            self.meyupe.append((
                related_names.name(),
                fake.teudat_zehut()
            ))
        self.labels = {
            "Full Name": {
                "font": "Arial", "font_size": 42,
                "color": "#3f3f3f",
                "text": full_name,
                'y_offset': -3,
            },
            "Account Number": {
                "font": "Arial", "font_size": 42,
                "color": "#3f3f3f",
                "text": account_number,
                'y_offset': 0
            },
            "Extra Account Data": {
                "font": "Arial", "font_size": 37,
                'color': '#2f2f2f',
                "text": fake.numerify("4444######_000# 000#"),
                'direction': 'ltr',
                'y_offset': 0
            },
            "Id Number": {
                "font": "Arial", "font_size": 42,
                "color": "#3f3f3f",
                "text": fake.teudat_zehut(),
                'y_offset': 0
            },
            "Print Date": {
                "font": "Arial", "font_size": 42,
                "color": "#0056b1",
                "text": fake.bank_statement_print_date("%d/%m/%Y"),
                'y_offset': 0
            },
            "Branch Name": {
                "font": "Arial", "font_size": 42,
                "color": "#3f3f3f",
                "text": str(branch.number),
                'y_offset': 1
            },
            "Extra ID": {
                "font": "Arial", "font_size": 42,
                "color": "#5f5f5f",
                "text": self.meyupe[0][1] if num_meyupe > 0 else '',
                'y_offset': -1,
                'x_offset': -1
            },
            "Extra Name": {
                "font": "Arial", "font_size": 42,
                "color": "#5f5f5f",
                "text": self.meyupe[0][0] if num_meyupe > 0 else '',
                'y_offset': -7,
                'x_offset': -2
            },
            "Account Date": {
                "font": "Arial", "font_size": 42,
                "color": "#5f5f5f",
                "text": fake.bank_account_creation_date("%d/%m/%Y") + ".",
                'y_offset': -2
            },
            "Account Number 2": {
                "font": "Arial", "font_size": 42,
                "color": "#5f5f5f",
                "text": account_number,
                'y_offset': 0,
                'x_offset': -8
            },
            "Branch Number": {
                "font": "Arial", "font_size": 42,
                "color": "#5f5f5f",
                "text": str(branch.number),
                'y_offset': 0
            },
            "Account Name": {
                "font": "Arial", "font_size": 42,
                "color": "#3f3f3f",
                "text": full_name,
                'y_offset': 0,
                'x_offset': -2
            },
        }

    def save(self, path):
        draw, draw_labels, image = self.save_init(
            path,
            'poalim_bank_statement',
            lambda item: item['bank'] == 'Poalim' and item['sttype'] == 'Private',
            self.labels
        )
        for label_id, label in draw_labels.items():
            self.draw_textbox(draw, **label)
        top_offset_y = 0
        if self.extra_names:
            extra_names_row_offset = 65
            top_offset_y += len(self.extra_names) * extra_names_row_offset
            self.copy_section(
                image, draw,
                top_y=draw_labels['Account Number 2']['y'] - 20,
                bottom_y=draw_labels['Account Number 2']['y'] + 1000,
                offset_y=len(self.extra_names) * extra_names_row_offset,
                fill='white'
            )
            idnum_label = draw_labels['Id Number']
            fullname_label = draw_labels['Full Name']
            offset_y = 0
            for extra in self.extra_names:
                offset_y += extra_names_row_offset
                self.copy_section(
                    image, draw,
                    top_y=fullname_label['y'] - 10,
                    bottom_y=fullname_label['y'] + 60,
                    offset_y=offset_y
                )
                name, tz = extra
                self.draw_textbox(draw, **{
                    **fullname_label,
                    'text': name, 'redraw': True,
                    'offset_y': offset_y
                })
                self.draw_textbox(draw, **{
                    **idnum_label,
                    'text': tz, 'redraw': True,
                    'offset_y': offset_y
                })
        if len(self.meyupe) > 1:
            extraid_label = draw_labels['Extra ID']
            extraname_label = draw_labels['Extra Name']
            offset_y = 0
            extra_section_top = 1659
            extra_section_bottom = 1729
            for m in self.meyupe[1:]:
                offset_y += extra_section_bottom - extra_section_top
                self.copy_section(
                    image, draw,
                    top_y=extra_section_top + top_offset_y,
                    bottom_y=extra_section_bottom + top_offset_y,
                    offset_y=offset_y
                )
                name, tz = m
                self.draw_textbox(draw, **{
                    **extraname_label,
                    'text': name, 'redraw': True,
                    'offset_y': offset_y + top_offset_y
                })
                self.draw_textbox(draw, **{
                    **extraid_label,
                    'text': tz, 'redraw': True,
                    'offset_y': offset_y + top_offset_y
                })
        elif len(self.meyupe) < 1:
            draw.rectangle((
                0, 1500 + top_offset_y, image.width, 2000 + top_offset_y
            ), fill="white")

        self.save_save(path, image)


class BankPoalim(Bank):
    name = 'הפועלים'

    def iterate_all_branches(self, **kwargs):
        with open(os.path.join(os.path.dirname(__file__), '..', 'data', 'poalim_branches.json'), encoding='utf-8') as f:
            for branch in json.load(f):
                if branch['branchTypeCode'] == 'PRV':
                    phone_number = None
                    for addr in branch['contactAddress']:
                        if addr['contactChannelTypeCode'] == 1 and len(addr.get('contactAddressInfo', '')) > 7:
                            phone_number = addr['contactAddressInfo']
                            break
                    for addr in branch['geographicAddress']:
                        city = addr.get('cityName')
                        street = addr.get('streetName')
                        building = addr.get('buildingNumber')
                        zip_code = addr.get('zipCode')
                        if all([city, street, building, zip_code]):
                            address = f'{street} {building}, {city}, {zip_code}'
                            break
                    yield BankBranch(
                        self, branch['branchName'], branch['branchNumber'],
                        phone_number=phone_number,
                        address=address,
                        manager_name=branch['branchManagerName'],
                        manager_phone_number=branch['branchManagerPhoneNumber'],
                        **kwargs
                    )

    def account_number(self):
        return self.provider.numerify('######')

    def statement(self, **kwargs):
        return BankStatementPoalim(self, **kwargs)
