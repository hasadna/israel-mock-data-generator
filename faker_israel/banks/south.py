import os
import json

from .bank import Bank, BankBranch, BankStatement, PRIVATE_DATA_PATH, _


class BankStatementSouth(BankStatement):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        fake = self.provider.generator
        branch = self.bank.branch()
        account_number = self.bank.account_number()
        related_names = fake.related_names()
        owner_name = related_names.name()
        print_date = fake.bank_statement_print_date()
        num_extra_names = fake.random_int(0, 4)
        self.extra_names = []
        for i in range(num_extra_names):
            self.extra_names.append((
                related_names.name(),
                fake.teudat_zehut()
            ))
        self.labels = {
            "Full Name": {
                "font": "Arial", "font_size": 50,
                "text": owner_name,
                'y_offset': 5,
                'x_offset': -7
            },
            "Account Number": {
                "font": "Arial", "font_size": 50,
                "text": account_number,
                'y_offset': 2
            },
            "Print Date": {
                "font": "Arial", "font_size": 50,
                "text": print_date.strftime('%d/%m/%Y'),
                'y_offset': -2,
            },
            "Extra Name": {
                "font": "Arial", "font_size": 50,
                "text": owner_name,
                'y_offset': -4,
            },
            "Extra ID": {
                "font": "Arial", "font_size": 50,
                "text": fake.teudat_zehut(),
                'y_offset': -2
            },
            "Ownership Type": {
                "font": "Arial", "font_size": 50,
                "text": "בעלים",
                'y_offset': -4
            },
            "Identification Type": {
                "font": "Arial", "font_size": 50,
                "text": "ת.ז.",
                'y_offset': -6
            },
            "IBAN": {
                "font": "Arial", "font_size": 50,
                "text": branch.iban(),
                'y_offset': -4
            },
            "Print Date/Time": {
                "font": "Arial", "font_size": 17.5,
                "text": print_date.strftime('%d %b %Y') + ' ' + fake.time('%H:%M:%S'),
                'direction': 'ltr',
                'y_offset': 1,
                'x_offset': 1
            },
            "Branch Number 2": {
                "font": "Arial", "font_size": 50,
                "text": branch.number,
                'center': True,
                'y_offset': -10
            },
            "Bank Name": {
                "font": "Arial", "font_size": 50,
                "text": f'בבנק הדרום בע"מ, בסניף {branch.number}',
                'y_offset': 3
            },
            "Bank Name 2": {
                "font": "Arial", "font_size": 50,
                "text": "בנק הדרום בע\"מ",
                'center': True,
                'y_offset': -10
            },
        }

    def save(self, path, **kwargs):
        draw, draw_labels, image = self.save_init(
            path,
            'south_bank_statement',
            lambda item: item['bank'] == _('South') and item['sttype'] == 'Private',
            self.labels
        )
        for label_id, label in draw_labels.items():
            self.draw_textbox(draw, **label)
        if self.extra_names:
            extra_names_row_offset = 60
            self.copy_section(
                image, draw,
                top_y=1690,
                bottom_y=2590,
                offset_y=len(self.extra_names) * extra_names_row_offset,
                fill='white'
            )
            name_label = draw_labels['Extra Name']
            id_label = draw_labels['Extra ID']
            offset_y = 0
            for extra in self.extra_names:
                offset_y += extra_names_row_offset
                self.copy_section(
                    image, draw,
                    top_y=1498,
                    bottom_y=1557,
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


class BankBranchSouth(BankBranch):

    def iban(self, bank_account_number=None):
        bank_account_number = bank_account_number or self.bank.account_number()
        return 'IL3601' + self.number.zfill(4) + '000000' + bank_account_number[:-3] + bank_account_number[-2:]


class BankSouth(Bank):
    name = 'לאומי'

    def iterate_all_branches(self, **kwargs):
        with open(os.path.join(PRIVATE_DATA_PATH, 'south_branches.json'), encoding='utf-8') as f:
            for item in f.read().split('"branch')[2:]:
                try:
                    item = json.loads('{"branch' + item[:-2] + '}}')
                except json.decoder.JSONDecodeError:
                    item = None
                if item:
                    branch = list(item.values())[0]
                    yield BankBranchSouth(
                        self, branch['name'], branch['number'],
                        phone_number='03-9545522',
                        address=f'{branch["address"]}, {branch["city"]}, {branch["zipCode"]}',
                        **kwargs
                    )

    def account_number(self):
        return self.provider.numerify('#####/##')

    def statement(self, **kwargs):
        return BankStatementSouth(self, **kwargs)
