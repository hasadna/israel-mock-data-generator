import json
from collections import OrderedDict

import dataflows as DF
from faker import Faker

from faker_israel import Provider as IsraelProvider


def test_faker():

    def iterator():
        for i in range(500):
            fake = Faker('he_IL')
            fake.add_provider(IsraelProvider)
            fake_data = OrderedDict()
            fake_data['family_name'] = fake.last_name()
            fake_data['first_name_1'] = fake.first_name()
            fake_data['first_name_2'] = fake.first_name()
            fake_data['tz_1'] = fake.teudat_zehut()
            fake_data['tz_2'] = fake.teudat_zehut()
            fake_data['company_name'] = company_name = fake.company()
            fake_data['company_name_p1'] = company_name[:11]
            fake_data['company_name_p2'] = company_name[11:]
            fake_data['het_pey'] = fake.het_pey()
            fake_data['address'] = fake.address()
            fake_data['bank_statement_print_date'] = fake.bank_statement_print_date('%d/%m/%Y')
            fake_data['bank_account_creation_date'] = fake.bank_account_creation_date('%d/%m/%Y')
            fake_data['bank_branch_address'] = fake.address()
            fake_data['bank_branch_phone_1'] = fake.phone_number()
            fake_data['bank_branch_phone_2'] = fake.phone_number()
            fake_data['bank_branch_phone_3'] = fake.phone_number()
            fake_data['bank_statement_print_time'] = fake.time('%H:%M')
            bank = fake.bank()
            bank_branch = bank.branch()
            fake_data['bank_name'] = fake.bank_name(bank)
            fake_data['branch_name'] = fake.bank_branch_name(bank_branch)
            fake_data['branch_number'] = fake.bank_branch_number(bank_branch)
            fake_data['account_number'] = fake.bank_account_number(bank)
            fake_data['iban'] = fake.bank_iban(bank)
            yield fake_data

    DF.Flow(
        iterator(),
        DF.dump_to_path('.data/bank_statements'),
        DF.printer(),
    ).process()
