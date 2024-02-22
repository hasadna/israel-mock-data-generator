import os
import datetime

from faker import Faker
from faker_israel import Provider as IsraelProvider
from faker_israel.banks import BANKS
from faker_israel.salaries import SALARIES


TYPES = {
    'bank': {
        'subtypes': BANKS,
        'generate': lambda fake, bank, png_path, pdf_path: fake.bank_statement(fake.bank(bank)).save(png_path, pdf_output_path=pdf_path),
        'test_generate': lambda fake, bank, kwargs: fake.bank_statement(fake.bank(bank), test=True, **kwargs).save('test.png'),
        'output_path': 'bank_statements',
    },
    'salary': {
        'subtypes': SALARIES,
        'generate': lambda fake, salary, png_path, pdf_path: fake.salary_slip(salary).save(png_path, pdf_output_path=pdf_path),
        'test_generate': lambda fake, salary, kwargs: fake.salary_slip(salary, test=True, **kwargs).save('test.png'),
        'output_path': 'salary_slips',
    }
}


def main(type_, subtype, num, test=False, **kwargs):
    fake = Faker('he_IL')
    fake.add_provider(IsraelProvider)
    type_config = TYPES.get(type_)
    assert type_config, f'Unknown type: {type_}'
    if subtype == 'all':
        selected_subtypes = list(type_config['subtypes'].keys())
    else:
        selected_subtypes = [s.strip() for s in subtype.split(',') if s.strip()]
    if test:
        assert len(selected_subtypes) == 1, 'Only one subtype can be specified for test mode'
        print(f'Generating 1 test {selected_subtypes[0]} {type_} to test.png')
        if kwargs:
            print(kwargs)
        type_config['test_generate'](fake, selected_subtypes[0], kwargs)
    else:
        output_path = os.path.join('.data', type_config['output_path'], datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
        print(f'Generating {num} {type_} items for {len(selected_subtypes)} subtypes to {output_path}')
        print(kwargs)
        for subtype in selected_subtypes:
            os.makedirs(os.path.join(output_path, subtype, 'png'))
            os.makedirs(os.path.join(output_path, subtype, 'pdf'))
            print(f'Generating {type_} items for {subtype}')
            for i in range(1, num+1):
                filename_template = '{i:0' + str(len(str(num))) + 'd}'
                png_output_path = os.path.join(output_path, subtype, 'png', filename_template.format(i=i)) + '.png'
                pdf_output_path = os.path.join(output_path, subtype, 'pdf', filename_template.format(i=i)) + '.pdf'
                type_config['generate'](fake, subtype, png_output_path, pdf_output_path)
