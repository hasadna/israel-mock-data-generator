import os
import json

from .bank import Bank, BankBranch


class BankBranchMizrahi(BankBranch):

    def iban(self, bank_account_number=None):
        branch_number = str(self.number)
        bank_account_number = str(bank_account_number or self.bank.account_number())
        return f'IL63 020{branch_number[0]} {branch_number[1:]}00 0000 0{bank_account_number[:3]} {bank_account_number[3:]}'


class BankMizrahi(Bank):
    name = 'מיזרחי טפחות'

    def iterate_all_branches(self, **kwargs):
        with open(os.path.join(os.path.dirname(__file__), '..', 'data', 'mizrahi_branches.json')) as f:
            for branch in json.load(f)["result"]:
                yield BankBranchMizrahi(
                    self, branch['ShemYeshuv'], branch['MisparSnif'],
                    phone_number=branch['Tel'],
                    address=f"{branch['Ktovet']}, {branch['ShemYeshuv']}",
                    manager_name=branch['ShemMenahel'],
                    **kwargs
                )

    def account_number(self):
        return self.provider.numerify('######')
