import json
import string
from typing import Dict

BANK_BRANCHES_CACHE = {}


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
