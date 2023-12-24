import os
import json

from .bank import Bank, BankBranch


class BankDiscount(Bank):
    name = 'דיסקונט'

    def iterate_all_branches(self, **kwargs):
        with open(os.path.join(os.path.dirname(__file__), '..', 'data', 'discount_branches.json'), encoding='utf-8') as f:
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
