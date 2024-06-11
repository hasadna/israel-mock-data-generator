import datetime
from dateutil.relativedelta import relativedelta

from .salary import Salary

from .. import common_draw, common



def get_rikuz_netunim_table(fake):
    res = []
    res.append([random_float(fake, 1, 99999)])   # סך כל התשלומים
    res.append([random_float(fake, 1, 99999)])   # ניכויי חובה מיסים
    res.append([random_float(fake, 1, 99999)])   # קופות גמל בהסכם
    res.append([random_float(fake, 1, 99999)])   # שכר נטו
    res.append([random_float(fake, 1, 99999)])   # ניכויי התחייבויות
    # perhaps following is not part of table? need to look in HTML...
    res.append([random_float(fake, 1, 99999)])   # נטו לתשלום
    return res

def get_pirtei_cheshbon_bank_table(fake):
    res = []
    mispar_cheshbon = fake.numerify('########')
    mispar_snif = fake.random_int(90, 999)
    mispar_bank = fake.random_int(10, 19)
    res.append([mispar_cheshbon, mispar_snif, mispar_bank])   
    return res

def random_float(fake, start, end):
    return f'{fake.random_int(100*start, 100*end)/100:,.2f}'


class SalaryEast(Salary):


    def generate(self):
        fake = self.fake
        machlaka_number = fake.random_int(50, 99999)
        fixed_context = {
            'teudat_zehut': fake.teudat_zehut(),
            'company_name': fake.company(),
            'company_address': f'{fake.street_address()}, {fake.city()}, {fake.postcode()}',
            'tik_nikuyim_number': fake.numerify("#########"),
            'company_number': fake.numerify("#########"),
            'machlaka_number': machlaka_number,
            # machlaka_name not described in IFYUN 
            'employee_name': fake.first_name() + ' ' + fake.last_name(),
            'employee_address': f'{fake.street_address()}',   
            'employee_address_city': f'{fake.city()}, {fake.postcode()}',
            'machlaka_number_employee': machlaka_number,

            'x1': fake.random_int(1, 10),
            'x1': fake.random_int(1, 10),
            'x1': fake.random_int(1, 10),
            'x1': fake.random_int(1, 10),
            'x1': fake.random_int(1, 10),
            'x1': fake.random_int(1, 10),
            'x1': fake.random_int(1, 10),
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
                render_path='salaries/east.html',
                page=self.html_page,
                http_server_port=self.subtype_context.http_server_port,
                width=2480, height=3507,
                context={
                    **fixed_context,
                    'salary_date': f'{salary_date.month} / {salary_date.year}',

                    #'zakaut_shnatit': fake.random_int(1, 30),

                    'netunim_golmyim_table': {
                        'div_trs_td_div': get_rikuz_netunim_table(fake)
                    },
                    'pirtey_cheshbon_table': {
                        'div_trs_td_div': get_pirtei_cheshbon_bank_table(fake)
                    },

                },
            )
