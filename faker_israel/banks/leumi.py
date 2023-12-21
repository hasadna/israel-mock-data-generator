import os
import json

from .bank import Bank, BankBranch


class BankBranchLeumi(BankBranch):

    def iban(self, bank_account_number=None):
        bank_account_number = bank_account_number or self.bank.account_number()
        return 'IL3601' + self.number.zfill(4) + '000000' + bank_account_number[:-3] + bank_account_number[-2:]


class BankLeumi(Bank):
    name = 'לאומי'

    def iterate_all_branches(self, **kwargs):
        with open(os.path.join(os.path.dirname(__file__), '..', 'data', 'leumi_branches.json')) as f:
            for item in f.read().split('"branch')[2:]:
                try:
                    item = json.loads('{"branch' + item[:-2] + '}}')
                except json.decoder.JSONDecodeError:
                    item = None
                if item:
                    branch = list(item.values())[0]
                    yield BankBranchLeumi(
                        self, branch['name'], branch['number'],
                        phone_number='03-9545522',
                        address=f'{branch["address"]}, {branch["city"]}, {branch["zipCode"]}',
                        **kwargs
                    )

    def account_number(self):
        return self.provider.numerify('#####/##')
