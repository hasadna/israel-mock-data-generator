import os
import datetime

from faker import Faker
from faker_israel import Provider as IsraelProvider


def main(bank, num, test=False, **kwargs):
    fake = Faker('he_IL')
    fake.add_provider(IsraelProvider)
    if test:
        print(f'Generating 1 test {bank} bank statement to test.png')
        if kwargs:
            print(kwargs)
        fake.bank_statement(fake.bank(bank), test=True, **kwargs).save('test.png')
    else:
        output_path = os.path.join('.data/bank_statements', bank, datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
        os.makedirs(output_path)
        print(f'Generating {num} {bank} bank statements to {output_path}')
        if kwargs:
            print(kwargs)
        for i in range(1, num+1):
            filename_template = '{i:0' + str(len(str(num))) + 'd}.png'
            fake.bank_statement(fake.bank(bank)).save(os.path.join(output_path, filename_template.format(i=i)))
