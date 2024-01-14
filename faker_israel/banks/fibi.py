import os
import json

from .bank import Bank, BankBranch, PRIVATE_DATA_PATH


class BankFibi(Bank):
    name = 'הבינלאומי'

    def iterate_all_branches(self, **kwargs):
        with open(os.path.join(PRIVATE_DATA_PATH, 'fibi_branches.json'), encoding='utf-8') as f:
            for city in json.load(f)["cities"]:
                if city['bank'] == 'sa_bank_fibi':
                    for branch in city['branches']:
                        yield BankBranch(
                            self, branch['name'], branch['number'],
                            address_city=city['title'],
                            **kwargs
                        )
