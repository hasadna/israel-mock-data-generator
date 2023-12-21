import datetime

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


class RelatedNames:

    def __init__(self, provider, relation_type=None, relation_type_elements=('none', 'none', 'family'), name_reverse=False):
        self.provider = provider
        relation_type = relation_type or provider.random_element(relation_type_elements)
        assert relation_type in ('none', 'family')
        self._last_name = provider.generator.last_name() if relation_type == 'family' else None
        self._name_reverse = name_reverse

    def faker_var_value_is_valid(self, faker_var_value):
        if self._last_name:
            # we verify that last name with additional 5 chars to allow for private name
            return faker_var_value.is_valid(self._last_name + ' 12345')
        else:
            return True

    def last_name(self):
        return self._last_name or self.provider.generator.last_name()

    def first_name(self):
        return self.provider.generator.first_name()

    def name(self):
        if self._name_reverse:
            return f'{self.last_name()} {self.first_name()}'
        else:
            return f'{self.first_name()} {self.last_name()}'


class Provider(BaseProvider):

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

    def bank_branch(self, bank=None, **kwargs):
        bank = bank or self.bank()
        return bank.branch(**kwargs)

    def bank_branch_name(self, bank_branch=None):
        bank_branch = bank_branch or self.bank_branch()
        return bank_branch.name

    def bank_branch_number(self, bank_branch=None):
        bank_branch = bank_branch or self.bank_branch()
        return bank_branch.number

    def bank_branch_address(self, bank_branch=None):
        bank_branch = bank_branch or self.bank_branch()
        return bank_branch.address

    def bank_account_number(self, bank=None):
        bank = bank or self.bank()
        return bank.account_number()

    def bank_statement_print_date(self, date_format=None):
        d = self.generator.date_this_year()
        return d if date_format is None else d.strftime(date_format)

    def bank_account_creation_date(self, date_format=None):
        d = self.generator.date_between_dates(datetime.date(1995, 1, 1), datetime.date(2022, 1, 1))
        return d if date_format is None else d.strftime(date_format)

    def bank_iban(self, bank_or_bank_branch=None, bank_account_number=None):
        bank_or_bank_branch = bank_or_bank_branch or self.bank()
        return bank_or_bank_branch.iban(bank_account_number)

    def teudat_zehut(self):
        nstr = self.generator.numerify('########')
        return nstr + tz_control_digit(nstr)

    def het_pey(self):
        return self.generator.numerify('5########')

    def related_names(self, **kwargs):
        return RelatedNames(self, **kwargs)

    def related_names_name(self, related_names=None):
        related_names = related_names or self.related_names()
        return related_names.name()

    def related_names_first_name(self, related_names=None):
        related_names = related_names or self.related_names()
        return related_names.first_name()

    def related_names_last_name(self, related_names=None):
        related_names = related_names or self.related_names()
        return related_names.last_name()
