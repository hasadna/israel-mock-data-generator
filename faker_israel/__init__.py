import string
import datetime
from typing import Dict

from faker.providers import BaseProvider
from faker.providers.company import Provider as CompanyProvider
from .banks import BANKS

from .company_he import CompanyHeProvider
from .address_he import AddressHeProvider
from .address_en import AddressEnProvider


def tz_control_digit(id_num):
    assert isinstance(id_num, str) and len(id_num) == 8
    total = 0
    for i in range(8):
        val = int(id_num[i]) # converts char to int
        if i%2 == 0:        # even index (0,2,4,6,8)
            total += val
        else:               # odd index (1,3,5,7,9)
            if val < 5:
                total += 2*val
            else:
                total += ((2*val)%10) + 1 # sum of digits in 2*val
                                          # 'tens' digit must be 1
    total = total%10            # 'ones' (rightmost) digit
    check_digit = (10-total)%10 # the complement modulo 10 of total
                                # for example 42->8, 30->0
    return str(check_digit)


class Provider(BaseProvider):
    ALPHA: Dict[str, str] = {c: str(ord(c) % 55) for c in string.ascii_uppercase}

    def __init__(self, generator):
        super().__init__(generator)
        self._locale = generator._Generator__config.get('locale')
        if self._locale in [None, 'he_IL']:
            self._lang = 'he'
        elif self._locale == 'en_US':
            self._lang = 'en'
        else:
            raise ValueError(f'Israel Provider Unsupported locale: {self._locale}')
        generator.add_provider({'he': CompanyHeProvider, 'en': CompanyProvider}[self._lang])
        generator.add_provider({'he': AddressHeProvider, 'en': AddressEnProvider}[self._lang])

    def bank(self, bank_id=None):
        if bank_id is None:
            bank = self.random_element(BANKS.values())(self)
        elif bank_id in BANKS:
            bank = BANKS[bank_id](self)
        else:
            raise ValueError(f'Unknown bank id: {bank_id}')
        return bank

    def bank_name(self, bank=None):
        bank = bank or self.bank()
        return bank.name

    def bank_full_name(self, bank=None):
        bank = bank or self.bank()
        return bank.full_name

    def bank_branch(self, bank=None):
        bank = bank or self.bank()
        return bank.branch()

    def bank_branch_name(self, bank_branch=None):
        bank_branch = bank_branch or self.bank_branch()
        return bank_branch.name

    def bank_branch_number(self, bank_branch=None):
        bank_branch = bank_branch or self.bank_branch()
        return bank_branch.number

    def bank_account_number(self, bank=None):
        bank = bank or self.bank()
        return bank.account_number()

    def bank_statement_print_date(self, date_format=None):
        d = self.generator.date_this_year()
        return d if date_format is None else d.strftime(date_format)

    def bank_account_creation_date(self, date_format=None):
        d = self.generator.date_between_dates(datetime.date(1995, 1, 1), datetime.date(2022, 1, 1))
        return d if date_format is None else d.strftime(date_format)

    def bank_iban(self, bank=None):
        bban = self.generator.bban()
        check = bban + "IL00"
        check_ = int("".join(self.ALPHA.get(c, c) for c in check))
        check_ = 98 - (check_ % 97)
        check = str(check_).zfill(2)
        return 'IL' + check + bban

    def teudat_zehut(self):
        nstr = self.generator.numerify('########')
        return nstr + tz_control_digit(nstr)

    def het_pey(self):
        return self.generator.numerify('5########')
