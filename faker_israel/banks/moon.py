import os
import json

from .bank import Bank, BankBranch, BankStatement, PRIVATE_DATA_PATH, _


class BankStatementMoon(BankStatement):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        fake = self.provider.generator
        print_date = fake.bank_statement_print_date('%d/%m/%Y')
        related_names = fake.related_names()
        branch = self.bank.branch()
        last_name = related_names.last_name()
        while True:
            first_name = related_names.first_name()
            if len(f'{last_name} {first_name}') < 20:
                break
        account_number = self.bank.account_number()
        num_extra_names = fake.random_int(0, 4)
        self.extra_names = []
        for i in range(num_extra_names):
            self.extra_names.append((
                related_names.first_name(),
                related_names.last_name(),
                fake.teudat_zehut()
            ))
        self.labels = {
            "Print Date/Time": {
                "font": "Arial", "font_size": 42,
                "text": print_date + " בשעה " + fake.time(pattern="%H:%M"),
                'y_offset': -1,
                'x_offset': 1,
            },
            "Full Name": {
                "font": "Arial", "font_size": 46,
                "text": first_name,
                'center': True,
                'y_offset': -3,
            },
            "Full Name 2": {
                "font": "Arial", "font_size": 46,
                "text": last_name,
                'center': True,
                'y_offset': -3,
            },
            "Id Number": {
                "font": "Arial", "font_size": 46,
                "text": fake.teudat_zehut(),
                'center': True,
                'y_offset': -3,
            },
            "Account Date": {
                "font": "Arial", "font_size": 46,
                'center': True,
                "text": fake.bank_account_creation_date("%d/%m/%Y"),
                'y_offset': -7,
            },
            "Branch Number": {
                "font": "Arial", "font_size": 46,
                'center': True,
                "text": str(branch.number),
                'y_offset': -7,
            },
            "Account Number": {
                "font": "Arial", "font_size": 46,
                'center': True,
                "text": account_number,
                'y_offset': -7,
            },
            "Extra Name": {
                "font": "Arial", "font_size": 45,
                'center': True,
                "text": f'{last_name} {first_name}',
                'y_offset': -7,
            },
            "IBAN": {
                "font": "Arial", "font_size": 37.5,
                'center': True,
                "text": branch.iban(account_number),
                'y_offset': -7,
            },
            "Print Date": {
                "font": "Arial", "font_size": 46,
                "text": print_date,
                'y_offset': 4,
            },
            "Bank Name": {
                "font": "Arial", "font_size": 46,
                "text": "בבנק הירח:",
                'y_offset': -8,
                'x_offset': -4
            },
            "Bank Number": {
                "font": "Arial", "font_size": 46,
                "text": "בנק הירח: MOONBNK",
                'y_offset': 4,
            },
            "Bank Name 2": {
                "font": "Arial", "font_size": 46,
                "text": "בנק הירח בע\"מ",
                'y_offset': 4,
            },
        }

    def save(self, path, **kwargs):
        draw, draw_labels, image = self.save_init(
            path,
            'moon_bank_statement',
            lambda item: item['bank'] == _('Moon') and item['sttype'] == 'Private',
            self.labels
        )
        for label_id, label in draw_labels.items():
            self.draw_textbox(draw, **label)
        if self.extra_names:
            extra_names_row_offset = 79
            self.copy_section(
                image, draw,
                top_y=1040,
                bottom_y=2020,
                offset_y=len(self.extra_names) * extra_names_row_offset,
                fill='white'
            )
            fullname_label = draw_labels['Full Name']
            fullname2_label = draw_labels['Full Name 2']
            idnum_label = draw_labels['Id Number']
            offset_y = 0
            for extra in self.extra_names:
                offset_y += extra_names_row_offset
                self.copy_section(
                    image, draw,
                    top_y=819,
                    bottom_y=899,
                    offset_y=offset_y
                )
                first_name, last_name, tz = extra
                self.draw_textbox(draw, **{
                    **fullname_label,
                    'text': first_name,
                    'offset_y': offset_y
                })
                self.draw_textbox(draw, **{
                    **fullname2_label,
                    'text': last_name,
                    'offset_y': offset_y
                })
                self.draw_textbox(draw, **{
                    **idnum_label,
                    'text': tz,
                    'offset_y': offset_y
                })
        self.save_save(path, image, **kwargs)


class BankBranchMoon(BankBranch):

    def iban(self, bank_account_number=None):
        branch_number = str(self.number)
        bank_account_number = str(bank_account_number or self.bank.account_number())
        return f'IL63 020{branch_number[0]} {branch_number[1:]}00 0000 0{bank_account_number[:3]} {bank_account_number[3:]}'


class BankMoon(Bank):
    name = 'הירח'

    def iterate_all_branches(self, **kwargs):
        with open(os.path.join(PRIVATE_DATA_PATH, 'moon_branches.json'), encoding='utf-8') as f:
            for branch in json.load(f)["result"]:
                yield BankBranchMoon(
                    self, branch['ShemYeshuv'], branch['MisparSnif'],
                    phone_number=branch['Tel'],
                    address=f"{branch['Ktovet']}, {branch['ShemYeshuv']}",
                    manager_name=branch['ShemMenahel'],
                    **kwargs
                )

    def account_number(self):
        return self.provider.numerify('######')

    def statement(self, **kwargs):
        return BankStatementMoon(self, **kwargs)
