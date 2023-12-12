import datetime

from faker.providers import BaseProvider
from faker.providers.company import Provider as CompanyProvider

from .company_he import CompanyHeProvider
from .address_he import AddressHeProvider
from .address_en import AddressEnProvider


BANKS = [
    {
        'name': 'אוצר החייל',
        'full_name': {
            'he': 'הבנק הבינלאומי הראשון לישראל בע"מ',
            'en': 'First Internation Israel Bank LTD'
        },
        'branch_name_prefix': 'אוצהח-',
    },
    {
        'name': 'דיסקונט',
    }
]


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

    def bank(self):
        bank = self.random_element(BANKS)
        return {
            k: v if isinstance(v, str) else v[self._lang]
            for k, v in bank.items()
        }

    def bank_name(self):
        return self.bank()['name']

    def bank_full_name(self):
        return self.bank().get('full_name', self.bank_name())

    def bank_branch_name(self, bank=None):
        bank = bank or self.bank()
        return bank.get('branch_name_prefix', '') + self.generator.city()

    def bank_branch_number(self, bank=None):
        return self.generator.numerify('###')

    def bank_account_number(self, bank=None):
        return self.generator.numerify('######')

    def bank_statement(self, bank=None):
        return {}

    def bank_statement_print_date(self, bank_statement=None, date_format='%d/%m/%Y'):
        return self.generator.date_this_year().strftime(date_format)

    def bank_statement_account_creation_date(self, bank_statement=None, date_format='%d/%m/%Y'):
        return self.generator.date_between_dates(datetime.date(1995, 1, 1), datetime.date(2022, 1, 1)).strftime(date_format)

    def teudat_zehut(self):
        return self.generator.numerify('#########')

    def het_pey(self):
        return self.generator.numerify('5########')
