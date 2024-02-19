import os
import json

from .bank import Bank, BankBranch, BankStatement, PRIVATE_DATA_PATH, _


class BankStatementNorth(BankStatement):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        fake = self.provider.generator
        related_names = fake.related_names()
        full_name = related_names.name()
        branch = self.bank.branch()
        account_number = self.bank.account_number()
        num_extra_names = fake.random_int(0, 4)
        self.extra_names = []
        for i in range(num_extra_names):
            self.extra_names.append((
                related_names.name(),
                fake.teudat_zehut()
            ))
        self.labels = {
            "Print Date": {
                "font": "Arial", "font_size": 33.3,
                "text": fake.bank_statement_print_date("%d/%m/%Y"),
            },
            "Full Name": {
                "font": "Arial", "font_size": 33.3,
                "text": full_name,
                'y_offset': -7
            },
            "Address": {
                "font": "Arial", "font_size": 33.3,
                "text": fake.parse("{{street_address}}, {{city}}"),
                'y_offset': -5
            },
            "Account Number": {
                "font": "Arial", "font_size": 33.3,
                "text": account_number,
                'y_offset': -3
            },
            "Old Account Number": {
                "font": "Arial", "font_size": 33.3,
                "text": fake.numerify('0-00-######'),
                'y_offset': -3
            },
            "Extra Account Data": {
                "font": "Arial", "font_size": 33.3,
                "text": fake.random_element([
                    "שירותי בריאות",
                    "הסתדרות המורים",
                    "עובדי מדינה",
                    "",
                ]),
                'y_offset': -3
            },
            "Branch Name": {
                "font": "Arial", "font_size": 33.3,
                "text": f'{branch.name} {branch.number}',
                'y_offset': -4
            },
            "Branch Address": {
                "font": "Arial", "font_size": 33.3,
                "text": branch.address,
                'y_offset': -10
            },
            "Branch Phone": {
                "font": "Arial", "font_size": 33.3,
                "text": branch.phone_number,
                'y_offset': -3
            },
            "Branch Fax": {
                "font": "Arial", "font_size": 33.3,
                "text": fake.numerify('0768######'),
                'y_offset': -3
            },
            "Branch Team": {
                "font": "Arial", "font_size": 33.3,
                "text": fake.random_element([
                    'אח"מ',
                    'פרטיים',
                    'עסקי'
                ]),
                'y_offset': -3
            },
            "Branch Phone 2": {
                "font": "Arial", "font_size": 33.3,
                "text": fake.numerify('0768######'),
                'y_offset': -3
            },
            "Account Number 2": {
                "font": "mriamc", "font_size": 38,
                'text': account_number,
                'y_offset': -3

            },
            "Full Name 2": {
                "font": "mriamc", "font_size": 38,
                'text': full_name,
            },
            "Id Number": {
                "font": "mriamc", "font_size": 38,
                'text': fake.teudat_zehut(),
            },
        }

    def save(self, path, **kwargs):
        draw, draw_labels, image = self.save_init(
            path,
            'north_bank_statement',
            lambda item: item['bank'] == _('North') and item['sttype'] == 'Private',
            self.labels
        )
        for label_id, label in draw_labels.items():
            font = self.draw_textbox(draw, **label)
            if label_id in ['Full Name 2', 'Id Number']:
                row_offset = 0
                for extra in self.extra_names:
                    row_offset += label['height']
                    text = extra[0] if label_id == 'Full Name 2' else extra[1]
                    if self.mock:
                        text = 'ללקקףףזזץץ'
                    left, top, right, bottom = font.getbbox(text, direction="rtl")
                    draw.text((label['x'] + label['width'] - right, label['y'] + label.get('y_offset', 0) + row_offset), text, fill=(0, 0, 0), font=font)
        self.save_save(path, image, **kwargs)


class BankNorth(Bank):
    name = 'הצפון'

    def iterate_all_branches(self, **kwargs):
        with open(os.path.join(PRIVATE_DATA_PATH, 'north_branches.json'), encoding='utf-8') as f:
            for branch in json.load(f):
                field_branch_street = branch['field_branch_street'].strip()
                if len(field_branch_street) <= 7:
                    yield BankBranch(
                        self, branch['name'], branch['field_branch_num'],
                        phone_number=branch['field_branch_phone'],
                        # address=f"{branch['field_branch_street']} {branch['field_branch_street_num']}, {branch['field_branch_city']['name']}",
                        address=field_branch_street,
                        manager_name=branch['field_manager_name'],
                        **kwargs
                    )

    def account_number(self):
        return self.provider.numerify('000#######')

    def statement(self, **kwargs):
        return BankStatementNorth(self, **kwargs)
