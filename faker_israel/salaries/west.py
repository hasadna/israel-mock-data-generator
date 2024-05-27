import datetime
import random
from dateutil.relativedelta import relativedelta

from .salary import Salary

from .. import common_draw, common

def pad_with_zeros(value, total_char_num):
    val = str(value)
    if len(val) < total_char_num:
        new_val = ((total_char_num - len(val)) * '0') + val
        return new_val
    else:
        return val

def empty_or(value):
    if random.choice([True, False]):
        return value;
    else:
        return ''

def random_float(fake, start, end):
    return f'{fake.random_int(100*start, 100*end)/100:,.2f}'


class SalaryWest(Salary):

    def generate(self):
        fake = self.fake

        tik_nikuyim_value = fake.numerify("#########")
        tik_bil_value = tik_nikuyim_value + '00'
        bank_num = fake.random_element(common.BANKS_NUMBERS.keys())
        bank_name = common.BANKS_NUMBERS[bank_num]

        fixed_context = {
            'company_name': fake.company(),
            'company_address': f'{fake.street_address()}',
            'company_address_city': f'{fake.city()}, {fake.postcode()}',
            'tik_nikuyim': tik_nikuyim_value,
            'company_number': fake.numerify("#########"),
            'tik_bil': tik_bil_value,

            'employee_name': fake.first_name() + ' ' + fake.last_name(),
            'employee_address': f'{fake.street_address()}',   #  f'{fake.city()}, {fake.postcode()}' ??
            # <=== ToDo: add element for city name and post code, currently hard-coded in the template
            #'employee_address': f'{fake.city()}, {fake.postcode()}',
            'id_number': fake.teudat_zehut(),
            'employee_number': fake.random_int(1, 9999),
            #'misra_sameh': '', # use default that is in template
            'misra_bil': fake.random_element(['עיקרית','מישנית']),
            'toshav': fake.random_element(['כן','לא']),
            'salary_base': fake.random_element(['חודשי','שעתי']),
            'part_job': f'{fake.random_int(10, 100, step=10) / 100:,.1f}' + '000',
            'vetek': fake.date_between(start_date='-30y', end_date='-5y').strftime('%d.%m.%y'),
            #'department': '',  # <========= ToDo: implement this
            'job_start': fake.date_between(start_date='-30y', end_date='-5y').strftime('%d/%m/%Y'), # <=== %Y is 4 digit year
            #'family_status': '',   # <========= ToDo: implement this
            'derug': pad_with_zeros(fake.random_int(0, 999),3),
            'darga': pad_with_zeros(fake.random_int(0, 999),3),
            'vetek_from': empty_or(fake.date_between(start_date='-30y', end_date='-5y').strftime('%d/%m/%Y')),
            'bank': str(bank_num) + '/' + str(fake.random_int(90, 999)),
            'account': fake.numerify('#######'),    

            'shovi_mas': random_float(fake, 0, 1000),       # <=== IFYUN did not specify the range, I made up 0-1000
            'tashlum_total': random_float(fake, 0, 30000),  # <=== IFYUN did not specify the range, I made up 0-30000
            
            'mandatory_nikuy': random_float(fake, 0, 3000),    # <=== IFYUN did not specify the range, I made up 0-3000

            'nikuyim_total': random_float(fake, -1000, 3000),    # <=== IFYUN did not specify the range, I made up -1000 - 3000,

            'salary_neto': random_float(fake, 0, 30000),  # <=== IFYUN did not specify the range, I made up 0-30000,

            # 'bank': '',
            # 'bank': '',
            # 'bank': '',
            # 'bank': '',
            # 'bank': '',
            # 'bank': '',

        }
        first_year = fake.random_int(2012, 2022)
        first_month = fake.random_int(1, 10)
        first_date = datetime.date(first_year, first_month, 1)
        for salary_date_num, salary_date in enumerate([
            first_date,
            first_date + relativedelta(months=1),
            first_date + relativedelta(months=2),
        ]):
            common_draw.save_render_html(
                output_path=self.item_context.png_output_path.replace('.png', f'-m{salary_date_num+1}.png'),
                pdf_output_path=self.item_context.pdf_output_path.replace('.pdf', f'-m{salary_date_num+1}.pdf') if self.item_context.pdf_output_path else None,
                render_path='salaries/west.html',
                page=self.html_page,
                http_server_port=self.subtype_context.http_server_port,
                width=2479, height=3508,
                context={
                    **fixed_context,
                    'salary_month': f'{salary_date.month}/{salary_date.year}',
                    'printed_at': f'10/{1+salary_date.month}/{salary_date.year}'

                },
            )
