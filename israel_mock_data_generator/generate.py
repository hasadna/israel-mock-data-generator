import os
import datetime
from contextlib import contextmanager

from faker import Faker
from faker_israel import Provider as IsraelProvider
from faker_israel.banks import BANKS
from faker_israel.salaries import SALARIES
from faker_israel.salaries.salary import salaries_generate_context, salary_generate_context, salary_item_generate_context


@contextmanager
def default_all_subtypes_context(**kwargs):
    yield {**kwargs}


@contextmanager
def default_subtype_context(all_subtypes_context, **kwargs):
    yield {
        **all_subtypes_context,
        **kwargs
    }


@contextmanager
def default_item_context(subtype_context, **kwargs):
    yield {
        **subtype_context,
        **kwargs,
    }


TYPES = {
    'bank': {
        'subtypes': BANKS,
        'generate': lambda item_context: item_context['fake'].bank_statement(item_context['fake'].bank(item_context['subtype'])).save(item_context['png_output_path'], pdf_output_path=item_context['pdf_output_path']),
        'test_generate': lambda item_context: item_context['fake'].bank_statement(item_context['fake'].bank(item_context['subtype']), **item_context).save('test.png'),
        'output_path': 'bank_statements',
    },
    'salary': {
        'subtypes': SALARIES,
        'all_subtypes_context': salaries_generate_context,
        'subtype_context': salary_generate_context,
        'item_context': salary_item_generate_context,
        'generate': lambda item_context: item_context.generate(),
        'output_path': 'salary_slips',
    }
}


def main(type_, subtype, num, test=False, test_pdf=False, **kwargs):
    fake = Faker('he_IL')
    fake.add_provider(IsraelProvider)
    type_config = TYPES.get(type_)
    assert type_config, f'Unknown type: {type_}'
    if subtype == 'all':
        selected_subtypes = list(type_config['subtypes'].keys())
    else:
        selected_subtypes = [s.strip() for s in subtype.split(',') if s.strip()]
    continue_ = kwargs.pop('continue', None)
    if continue_:
        assert not test
        assert len(selected_subtypes) == 1
        continue_pathdate, continue_num = continue_.split(',')
        continue_num = int(continue_num)
    else:
        continue_pathdate, continue_num = None, None
    with type_config.get('all_subtypes_context', default_all_subtypes_context)(fake=fake) as all_subtypes_context:
        if test or test_pdf:
            assert len(selected_subtypes) == 1, 'Only one subtype can be specified for test mode'
            subtype = selected_subtypes[0]
            subtype_class = type_config['subtypes'][subtype]
            with type_config.get('subtype_context', default_subtype_context)(all_subtypes_context, subtype=selected_subtypes[0], subtype_class=subtype_class, test=True, test_pdf=test_pdf) as subtype_context:
                print(f'Generating 1 test {selected_subtypes[0]} {type_} to test.' + ('pdf' if test_pdf else 'png'))
                if kwargs:
                    print(kwargs)
                with type_config.get('item_context', default_item_context)(subtype_context, **kwargs) as item_context:
                    type_config.get('test_generate', type_config['generate'])(item_context)
        else:
            output_path = os.path.join('.data', type_config['output_path'], continue_pathdate or datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
            print(f'Generating {num} {type_} items for {len(selected_subtypes)} subtypes to {output_path}')
            if continue_num:
                print(f'Continuing from {continue_num}')
            print(kwargs)
            for subtype in selected_subtypes:
                subtype_class = type_config['subtypes'][subtype]
                with type_config.get('subtype_context', default_subtype_context)(all_subtypes_context, subtype=subtype, subtype_class=subtype_class) as subtype_context:
                    if continue_:
                        os.makedirs(os.path.join(output_path, subtype, 'png'), exist_ok=True)
                        os.makedirs(os.path.join(output_path, subtype, 'pdf'), exist_ok=True)
                    else:
                        os.makedirs(os.path.join(output_path, subtype, 'png'))
                        os.makedirs(os.path.join(output_path, subtype, 'pdf'))
                    print(f'Generating {type_} items for {subtype}')
                    for i in range(continue_num or 1, num+1):
                        filename_template = '{i:0' + str(len(str(num))) + 'd}'
                        with type_config.get('item_context', default_item_context)(subtype_context, **{
                            'i': i,
                            'png_output_path': os.path.join(output_path, subtype, 'png', filename_template.format(i=i)) + '.png',
                            'pdf_output_path': os.path.join(output_path, subtype, 'pdf', filename_template.format(i=i)) + '.pdf',
                        }) as item_context:
                            type_config['generate'](item_context)
