import os
import datetime

from faker import Faker
from faker_israel import Provider as IsraelProvider
from faker_israel.banks import BANKS


def main(bank, num, test=False, **kwargs):
    fake = Faker('he_IL')
    fake.add_provider(IsraelProvider)
    if bank == 'all':
        banks = [b for b in BANKS.keys() if b not in ['fibi']]
    else:
        banks = [b.strip() for b in bank.split(',') if b.strip()]
    if test:
        assert len(banks) == 1, 'Only one bank can be specified for test mode'
        print(f'Generating 1 test {bank} bank statement to test.png')
        if kwargs:
            print(kwargs)
        fake.bank_statement(fake.bank(bank), test=True, **kwargs).save('test.png')
    else:
        output_path = os.path.join('.data/bank_statements', datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
        print(f'Generating {num} bank statements for {len(banks)} banks to {output_path}')
        print(kwargs)
        for bank in banks:
            os.makedirs(os.path.join(output_path, bank, 'png'))
            os.makedirs(os.path.join(output_path, bank, 'pdf'))
            print(f'Generating bank statements for {bank}')
            for i in range(1, num+1):
                filename_template = '{i:0' + str(len(str(num))) + 'd}'
                png_output_path = os.path.join(output_path, bank, 'png', filename_template.format(i=i)) + '.png'
                pdf_output_path = os.path.join(output_path, bank, 'pdf', filename_template.format(i=i)) + '.pdf'
                fake.bank_statement(fake.bank(bank)).save(png_output_path, pdf_output_path=pdf_output_path)
