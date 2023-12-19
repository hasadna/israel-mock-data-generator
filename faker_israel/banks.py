import os
import json
import string
from typing import Dict
from functools import partial


BANK_BRANCHES_CACHE = {}


class Bank:
    ALPHA: Dict[str, str] = {c: str(ord(c) % 55) for c in string.ascii_uppercase}

    def __init__(self, id_, provider):
        self.id = id_
        self.provider = provider

    def branch(self):
        if self.id not in BANK_BRANCHES_CACHE:
            BANK_BRANCHES_CACHE[self.id] = list(self.iterate_all_branches())
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


class BankBranch:

    def __init__(self, bank, name, number, phone_number=None, address=None, manager_name=None, manager_phone_number=None, address_city=None):
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


class BankPoalim(Bank):
    name = 'הפועלים'

    def iterate_all_branches(self):
        with open(os.path.join(os.path.dirname(__file__), 'data', 'poalim_branches.json')) as f:
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
                    )


class BankBranchLeumi(BankBranch):

    def iban(self, bank_account_number=None):
        bank_account_number = bank_account_number or self.bank.account_number()
        return 'IL3601' + self.number.zfill(4) + '000000' + bank_account_number[:-3] + bank_account_number[-2:]


class BankLeumi(Bank):
    name = 'לאומי'

    def iterate_all_branches(self):
        with open(os.path.join(os.path.dirname(__file__), 'data', 'leumi_branches.json')) as f:
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
                    )

    def account_number(self):
        return self.provider.numerify('#####/##')


class BankDiscount(Bank):
    name = 'דיסקונט'

    def iterate_all_branches(self):
        with open(os.path.join(os.path.dirname(__file__), 'data', 'discount_branches.json')) as f:
            for branch in json.load(f):
                yield BankBranch(
                    self, branch['name'], branch['field_branch_num'],
                    phone_number=branch['field_branch_phone'],
                    address=f"{branch['field_branch_street']} {branch['field_branch_street_num']}, {branch['field_branch_city']['name']}",
                    manager_name=branch['field_manager_name']
                )


class BankMizrahi(Bank):
    name = 'מיזרחי טפחות'

    def iterate_all_branches(self):
        with open(os.path.join(os.path.dirname(__file__), 'data', 'mizrahi_branches.json')) as f:
            for branch in json.load(f)["result"]:
                yield BankBranch(
                    self, branch['ShemYeshuv'], branch['MisparSnif'],
                    phone_number=branch['Tel'],
                    address=f"{branch['Ktovet']}, {branch['ShemYeshuv']}",
                    manager_name=branch['ShemMenahel']
                )


class BankFibi(Bank):
    name = 'הבינלאומי'

    def iterate_all_branches(self):
        with open(os.path.join(os.path.dirname(__file__), 'data', 'fibi_branches.json')) as f:
            for city in json.load(f)["cities"]:
                if city['bank'] == 'sa_bank_fibi':
                    for branch in city['branches']:
                        yield BankBranch(
                            self, branch['name'], branch['number'],
                            address_city=city['title'],
                        )


BANKS = {k: partial(v, k) for k, v in {
    'poalim': BankPoalim,
    'leumi': BankLeumi,
    'discount': BankDiscount,
    'mizrahi': BankMizrahi,
    'fibi': BankFibi,
}.items()}
