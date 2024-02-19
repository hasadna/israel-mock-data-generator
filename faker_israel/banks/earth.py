import os
import json

from .bank import Bank, BankBranch, BankStatement, PRIVATE_DATA_PATH, _


class BankStatementEarth(BankStatement):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        fake = self.provider.generator
        account_number = self.bank.account_number()
        branch = self.bank.branch()
        related_names = fake.related_names(name_reverse=True)
        owner_name = related_names.name()
        num_extra_names = fake.random_int(0, 4)
        self.extra_names = []
        for i in range(num_extra_names):
            self.extra_names.append((
                related_names.name(),
                fake.teudat_zehut()
            ))
        self.labels = {
            "Account Number": {
                "font": "Arial", "font_size": 42,
                "text": f"25-{branch.number}-{account_number}",
                'y_offset': 3, 'x_offset': -1,
            },
            "Print Date/Time": {
                "font": "Arial", "font_size": 42,
                "text": fake.bank_statement_print_date('%d/%m/%Y') + ', ' + fake.time('%H:%M'),
                'direction': 'ltr',
                'y_offset': 5, 'x_offset': 0,
            },
            "Full Name": {
                "font": "Arial", "font_size": 42,
                "text": owner_name,
                'y_offset': -6, 'x_offset': -1,
            },
            "Branch Number": {
                "font": "Arial", "font_size": 42,
                "text": branch.number,
                'y_offset': 2, 'x_offset': 0,
            },
            "Account Number 2": {
                "font": "Arial", "font_size": 42,
                "text": account_number,
                'y_offset': 5, 'x_offset': -5,
            },
            "Full Name 2": {
                "font": "Arial", "font_size": 42,
                "text": owner_name,
                'y_offset': 3, 'x_offset': -1,
            },
            "Id Number": {
                "font": "Arial", "font_size": 42,
                "text": fake.teudat_zehut(),
                'y_offset': 4, 'x_offset': -1,
            },
            "Branch Number 2": {
                "font": "Arial", "font_size": 42,
                "text": branch.number,
                'y_offset': 3, 'x_offset': -1,
            },
            "Extra Account Data": {
                "font": "Arial", "font_size": 42,
                "text": account_number,
                'y_offset': 3, 'x_offset': -5,
            },
            "Account Date": {
                "font": "Arial", "font_size": 42,
                "text": fake.bank_account_creation_date('%d/%m/%Y'),
                'y_offset': 7, 'x_offset': -1,
            },
            "Bank Number": {
                "font": "Arial", "font_size": 42,
                "text": "25",
                'y_offset': 7, 'x_offset': -3,
            },
            "Bank Name": {
                "font": "Arial", "font_size": 42,
                "text": "בנק האדמה",
                'y_offset': 7, 'x_offset': -10,
            },

        }

    def save(self, path, **kwargs):
        draw, draw_labels, image = self.save_init(
            path,
            'earth_bank_statement',
            lambda item: item['bank'] == _('Earth') and item['sttype'] == 'Private',
            self.labels
        )
        for label_id, label in draw_labels.items():
            self.draw_textbox(draw, **label)
        if self.extra_names:
            extra_names_row_offset = 118
            self.copy_section(
                image, draw,
                top_y=1529,
                bottom_y=2182,
                offset_y=len(self.extra_names) * extra_names_row_offset,
                fill='white'
            )
            name_label = draw_labels['Full Name 2']
            id_label = draw_labels['Id Number']
            offset_y = 0
            for extra in self.extra_names:
                offset_y += extra_names_row_offset
                self.copy_section(
                    image, draw,
                    top_y=1407,
                    bottom_y=1526,
                    offset_y=offset_y
                )
                name, tz = extra
                self.draw_textbox(draw, **{
                    **name_label,
                    'text': name,
                    'offset_y': offset_y
                })
                self.draw_textbox(draw, **{
                    **id_label,
                    'text': tz,
                    'offset_y': offset_y
                })
        self.save_save(path, image, **kwargs)


class BankBranchEarth(BankBranch):
    pass


class BankEarth(Bank):
    name = 'האדמה'

    def iterate_all_branches(self, **kwargs):
        with open(os.path.join(PRIVATE_DATA_PATH, 'earth_branches.json'), encoding='utf-8') as f:
            for branch in json.load(f)["branches"]:
                yield BankBranchEarth(
                    self, branch['branchName'], branch['branchNumber'],
                    phone_number=branch['branchPhones'][0],
                    address=f"{branch['branchLocationName']}, {branch['branchCity']}",
                    **kwargs
                )

    def account_number(self):
        return self.provider.numerify('######')

    def statement(self, **kwargs):
        return BankStatementEarth(self, **kwargs)
