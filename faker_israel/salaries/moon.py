import datetime
import random
from dateutil.relativedelta import relativedelta

from .salary import Salary

from .. import common_draw, common


def get_nikuy_mutavim_table(fake):
    res = []
    descs = set([
        'ועד סגל זוטר',
        'קו הבריאות',
        'תשלומים לעירייה',
        'ביטוח שיניים',
        'החזרי הלוואות',
        'מגדל קה"ש',
        'איילון מיטיב',
        'אלטשולר שחם',
        'אנליסט גמל',
        'הפניקס גמל',
        'מגדל לתגמולים',
        'מור מנורה',
        'קחצ"ק_מניות',
        'קחצ"ק_הראל',
        'ילין לפידות',
        'הפניקס כללי',
        'אינפיניטי',
    ])
    for i in range(3):
        desc = fake.random_element(list(descs))
        descs.remove(desc)
        with_dates = fake.random_int(0, 1) == 0
        res.append([
            fake.numerify('######-#'),
            desc,
            fake.numerify('######') if fake.random_int(0, 2) == 0 else '',
            fake.numerify('#.##') if fake.random_int(0, 1) == 0 else '',
            fake.random_int(1, 3000) if fake.random_int(0, 3) == 0 else '',
            fake.date('%m/%Y') if with_dates else '',
            fake.date('%m/%Y') if with_dates else '',
            f'{fake.random_int(0, 100000) / 100:.2f}',
        ])
    return res


class SalaryMoon(Salary):

    def generate(self):
        fake = self.fake
        tik_nikuim = fake.numerify('#########')
        fixed_context = {
            'full_name': fake.name(),
            'personal_id': fake.teudat_zehut(),
            'personal_details_office': fake.numerify('###'),
            'personal_details_address': fake.address(),
            'personal_details_marital_status': fake.random_element(['רווק\ה', 'גרוש\ה', 'אלמן\ה', 'נשוי\אה']),
            'personal_details_tax_percentage': fake.random_int(10, 50),
            'personal_details_status': fake.random_element(['עובד', 'גימלאי']),
            'personal_details_bank': fake.random_element([
                '12 - בנק הפועלים',
                '20 - בנק מזרחי טפחות',
                '11 - בנק דיסקונט',
                '31 - בנק יהב',
                '10 - בנק הדואר',
                '23 - בנק פועלי אגוד',
                '17 - בנק לאומי',
                '46 - בנק מרכנתיל',
            ]),
            'personal_details_branch': fake.numerify('###') + ' - ' + fake.city(),
            'company_name': fake.company(),
            'bank_account_number': fake.numerify('#######'),
            'tik_nikuyim': tik_nikuim,
            'bituah_leumi': tik_nikuim,
        }
        first_year = fake.random_int(2012, 2022)
        first_month = fake.random_int(1, 10)
        first_date = datetime.date(first_year, first_month, 1)
        for salary_date_num, salary_date in enumerate([
            first_date,
            first_date + relativedelta(months=1),
            first_date + relativedelta(months=2),
        ]):
            month = salary_date.strftime('%m')
            year = salary_date.strftime('%Y')
            month_name_heb = fake.month_name_he(month)
            work_months_start = fake.random_int(1, first_month)
            work_months_end = fake.random_int(first_month+1, 12)
            common_draw.save_render_html(
                output_path=self.item_context.png_output_path.replace('.png', f'-m{salary_date_num+1}.png'),
                pdf_output_path=self.item_context.pdf_output_path.replace('.pdf', f'-m{salary_date_num+1}.pdf') if self.item_context.pdf_output_path else None,
                render_path='salaries/moon.html',
                page=self.html_page,
                http_server_port=self.subtype_context.http_server_port,
                width=2705, height=3600,
                output_scale=0.3,
                context={
                    **fixed_context,
                    'month_year': f'{month_name_heb} {year}',
                    'tlush': fake.numerify('#####'),
                    'nikuy_mutavim_table': {
                        'div_trs_td_div': get_nikuy_mutavim_table(fake)
                    },
                    **{
                        f'nikuy_hova_{j+1}': f'{fake.random_int(-200000, 200000) / 100:.2f}'
                        for j in range(6)
                    },
                    'total_nikuy_hova': f'{fake.random_int(-200000, 200000) / 100:.2f}',
                    'bruto_shotef': f'{fake.random_int(100, 3000000)/100:.2f}',
                    'sum_nikuy_mutav': f'{fake.random_int(100, 3000000)/100:.2f}',
                    'total_nikuy_mutav': f'{fake.random_int(100, 3000000)/100:.2f}',
                    'total_bank_shekel': f'{fake.random_int(300000, 5000000)/100:.2f}',
                    **{
                        f'aggregate_tax_{j+1}': f'{fake.random_int(0, 3000000) / 100:.2f}'
                        for j in range(4)
                    },
                    **{
                        f'work_months_{j+1}': str(j+1) if j+1 in range(work_months_start, work_months_end+1) else ''
                        for j in range(12)
                    },
                    **{
                        f'work_months_val_{j+1}': '25' if j+1 in range(work_months_start, work_months_end+1) else ''
                        for j in range(12)
                    },
                    'nikuy_bituah_leumi': f'{fake.random_int(100, 1000000)/100:.2f}',
                    'bruto_mas': f'{fake.random_int(100, 30000000)/100:.2f}',
                    'nikuy_bb': f'{fake.random_int(100, 1000000)/100:.2f}',
                    'mas_hahnasa': f'{fake.random_int(100, 1000000)/100:.2f}',
                    'seif_45': f'{fake.random_int(100, 1000000)/100:.2f}',
                    'tashlumim_shnatiim': f'{fake.random_int(100, 1000000)/100:.2f}',
                    'bruto_bl': f'{fake.random_int(100, 30000000)/100:.2f}',
                    'hafrasha_bl': f'{fake.random_int(100, 1000000)/100:.2f}',
                    'yesod_meshulav': f'{fake.random_int(100, 9900000)/100:.2f}' if fake.random_int(0, 1) == 0 else '',
                    'tosefet': f'{fake.random_int(100, 9900000)/100:.2f}' if fake.random_int(0, 1) == 0 else '',
                    'extra_work': f'{fake.random_int(100, 9900000)/100:.2f}' if fake.random_int(0, 1) == 0 else '',
                    'reimbursment': f'{fake.random_int(100, 9900000)/100:.2f}' if fake.random_int(0, 1) == 0 else '',
                    'other_tashlumim': f'{fake.random_int(100, 9900000)/100:.2f}' if fake.random_int(0, 1) == 0 else '',
                    'bruto_shotef_down': f'{fake.random_int(100, 9900000)/100:.2f}' if fake.random_int(0, 1) == 0 else '',
                    'hefreshim': f'{fake.random_int(100, 9900000)/100:.2f}' if fake.random_int(0, 1) == 0 else '',
                    'total_tashlumim_down': f'{fake.random_int(100, 9900000)/100:.2f}' if fake.random_int(0, 1) == 0 else '',
                    'nikuyey_hova': f'{fake.random_int(100, 9900000)/100:.2f}' if fake.random_int(0, 1) == 0 else '',
                    'sachar_neto': f'{fake.random_int(100, 9900000)/100:.2f}' if fake.random_int(0, 1) == 0 else '',
                    'nekuyey_reshut': f'{fake.random_int(100, 9900000)/100:.2f}' if fake.random_int(0, 1) == 0 else '',
                    'nikuy_mos': f'{fake.random_int(100, 9900000)/100:.2f}' if fake.random_int(0, 1) == 0 else '',
                    'schum_babank': f'{fake.random_int(100, 9900000)/100:.2f}' if fake.random_int(0, 1) == 0 else '',
                },
            )
