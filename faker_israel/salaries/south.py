import datetime
from dateutil.relativedelta import relativedelta

from .salary import Salary

from .. import common_draw, common


TASHLUMS = [
    'שכר חודשי',
    'שעות חסר',
    'נסיעות מדווח',
    'נסיעות החזר חודשי',
    'טלפון',
    'תשלום שיחות טלפון',
    'תן ביס',
    'קורס/לימודים',
    'השתלמות',
    'נופש',
    'מקדמות שכר',
    'החזר נסיעות חול',
    'החזר נסיעות דלק',
    'מוניות',
    'הוצאות אחרות',
    'ביגוד',
]

NIKUY_RESHUT = [
    'קו הבריאות',
    'תשלומים לעירייה',
    'ביטוח שיניים',
    'החזרי הלוואות',
    'השתתפות בקורס',
]


def empty_or_int(fake, from_, to, num_false=2):
    if fake.random_element([*[False for _ in range(num_false)], True]):
        return str(fake.random_int(from_, to))
    else:
        return '&nbsp;'


def empty_or_float(fake, from_, to, num_false=2):
    if fake.random_element([*[False for _ in range(num_false)], True]):
        return float_string(fake, from_, to)
    else:
        return '&nbsp;'


def float_string(fake, from_, to):
    num = fake.random_int(from_*100, to*100)/100
    return f'{num:,.2f}'


def get_tashlumim_table(fake):
    tashlums = set(TASHLUMS)
    res = []
    for i in range(fake.random_int(3, 12)):
        tashlum = fake.random_element(tashlums)
        tashlums.remove(tashlum)
        res.append([
            tashlum,
            f'{fake.random_element(["", "", "-"])}{fake.random_int(1, 99999)/100:.2f}' if fake.random_element([False, False, True]) else '&nbsp;',
            empty_or_float(fake, 1, 9999.99),
            empty_or_float(fake, 1, 100),
            empty_or_float(fake, 500, 50000),
            empty_or_float(fake, 500, 5000),
        ])
    if len(res) < 12:
        for i in range(12-len(res)):
            res.append(['&nbsp;', '&nbsp;', '&nbsp;', '&nbsp;', '&nbsp;', '&nbsp;'])
    return res


def get_nikuy_reshut_table(fake):
    res = []
    avail_nikuy_reshut = set(NIKUY_RESHUT)
    for i in range(fake.random_int(0, 5)):
        nikuy_reshut = fake.random_element(avail_nikuy_reshut)
        avail_nikuy_reshut.remove(nikuy_reshut)
        res.append([
            nikuy_reshut,
            f'{fake.random_element(["", "", "-"])}{fake.random_int(1, 999999) / 100:.2f}' if fake.random_element([False, False, True]) else '&nbsp;',
            f'{fake.random_element(["", "", "-"])}{fake.random_int(1, 999)}' if fake.random_element([False, False, True]) else '&nbsp;',
            f'{fake.random_element(["", "", "-"])}{fake.random_int(1, 999999) / 100:.2f}' if fake.random_element([False, False, True]) else '&nbsp;',
        ])
    add_total = len(res) > 0
    for i in range(8 - len(res) if add_total else 9):
        res.append(['&nbsp;', '&nbsp;', '&nbsp;', '&nbsp;'])
    if add_total:
        res.append([
            'סה"כ',
            f'{fake.random_element(["", "", "-"])}{fake.random_int(1, 999999) / 100:.2f}' if fake.random_element([False, False, True]) else '&nbsp;',
            f'{fake.random_element(["", "", "-"])}{fake.random_int(1, 999)}' if fake.random_element([False, False, True]) else '&nbsp;',
            f'{fake.random_element(["", "", "-"])}{fake.random_int(1, 999999) / 100:.2f}' if fake.random_element([False, False, True]) else '&nbsp;',
        ])
    return res


def get_headruiot_hodashim_row(fake):
    month_from = fake.random_int(1, 4)
    month_final_to = fake.random_int(7, 12)
    month_to = fake.random_int(month_from, month_final_to)
    months = []
    for i in range(1, 13):
        if month_to < i <= month_final_to:
            months.append('ל')
        elif i > month_final_to:
            months.append('&nbsp;')
        else:
            months.append('כ')
    return reversed(months)


def get_netunim_miztabrim_table(fake):
    res = []
    for i in range(8):
        if i == 5:
            res.append(['&nbsp;', '&nbsp;', '&nbsp;'])
        else:
            res.append([
                empty_or_float(fake, 1, 99999.99),
                empty_or_float(fake, 1, 99999.99),
                empty_or_float(fake, 1, 99999.99),
            ])
    return res


class SalarySouth(Salary):

    def generate(self):
        fake = self.fake
        top_salary_account_text = '&nbsp;'
        top_salary_account_num = '&nbsp;'
        if fake.random_element([False, False, True]):
            top_salary_account_num = fake.numerify('########')
        else:
            top_salary_account_text = 'משולם לעובד'
        num_kids = fake.random_int(0, 9)
        fixed_context = {
            'topheader_company_name': fake.company(),
            'topheader_company_address': f'{fake.street_address()}, {fake.city()}&nbsp;&nbsp;{fake.postcode()}',
            'topheader_address': f'{fake.street_address()}, {fake.city()}&nbsp;&nbsp;{fake.postcode()}',
            'topheader_tiknikuim_bl': fake.numerify('#########00'),
            'topheader_tiknikuim_mh': fake.numerify('#########'),
            'topheader_tiknikuim_mispar_taagid': 'מספר תאגיד - ' + str(fake.het_pey()),

            'top_employee_number': str(fake.random_int(1, 9999)),
            'top_employee_mahlaka': str(fake.random_int(0, 9999)),
            'top_employee_last_name': fake.last_name(),
            'top_employee_first_name': fake.first_name(),
            'top_employee_tz': fake.teudat_zehut(),
            'top_employee_tatmahlaka': empty_or_int(fake, 0, 999),
            'top_employee_derug': empty_or_int(fake, 0, 999),
            'top_employee_darga': empty_or_int(fake, 0, 999),
            'top_employee_vetek_days': str(fake.random_int(0, 31)),
            'top_employee_vetek_months': str(fake.random_int(0, 12)),
            'top_employee_vetek_years': str(fake.random_int(0, 30)),
            'top_employee_workstart': fake.date_between(start_date='-30y', end_date='-3y').strftime('%d/%m/%y'),

            'top_salary_taarif': str(fake.random_int(100, 5000)),
            'top_salary_taarif_day': str(fake.random_int(100, 5000)),
            'top_salary_taarif_hour': str(fake.random_int(25, 600)),
            'top_salary_bank': str(fake.random_element(common.BANKS_NUMBERS.values())) if fake.random_element([False, False, True]) else '&nbsp;',
            'top_salary_branch': empty_or_int(fake, 90, 999),
            'top_salary_account_text': top_salary_account_text,
            'top_salary_account_num': top_salary_account_num,

            'netunim_nosafim_mazav_mishpahti': fake.random_element(['נ', 'ג', 'א', 'ר']) + ('' if num_kids == 0 else f'+{num_kids}'),
            'netunim_nosafim_working_partner': fake.random_element(['כ', 'ל', '&nbsp;']),
            'netunim_nosafim_n_zikui': f'{fake.random_element(range(0, 600, 25))/100:.2f}',
            'netunim_nosafim_ahuz_misra': '&nbsp;',
            'netunim_nosafim_mas_shuli': float_string(fake, 0, 30),
            'netunim_nosafim_mas_kavua': '&nbsp;',
            'netunim_nosafim_zikui_ishi': str(fake.random_int(1, 999)),
            'netunim_nosafim_zikui_nosaf': '&nbsp;',
            'netunim_nosafim_zikui_gemel': '&nbsp;',
            'netunim_nosafim_zikui_mishmarot': '&nbsp;',
            'netunim_nosafim_ptor_hodshi': '&nbsp;',
            'netunim_nosafim_ptor_s47': '&nbsp;',
            'netunim_nosafim_zikui_hanahat_pituach': '&nbsp;',
            'netunim_nosafim_teum_mas': fake.random_element(['כ', 'ל']),
            'netunim_nosafim_sahar_leteum': '&nbsp;',
            'netunim_nosafim_mh_leteum': '&nbsp;',
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
                render_path='salaries/south.html',
                page=self.html_page,
                http_server_port=self.subtype_context.http_server_port,
                width=2479, height=3504,
                context={
                    **fixed_context,
                    'topheader_slip_date': salary_date.strftime('%-m/%Y'),
                    'top_salary_workdays': f'{fake.random_int(0, 31)}/{fake.random_int(0, 31)}',
                    'top_salary_workhours': str(fake.random_int(0, 300)),

                    'netunim_nosafim_pizuim_hodshi': float_string(fake, 0, 9999.99),
                    'netunim_nosafim_pizuim_ptor': float_string(fake, 0, 9999.99),
                    'netunim_nosafim_pizuim_vatika': float_string(fake, 0, 9999.99),
                    'netunim_nosafim_sahar_lepizuim': float_string(fake, 0, 9999.99),
                    'netunim_nosafim_kopag_maasik_hodshi': float_string(fake, 0, 9999.99),
                    'netunim_nosafim_sahar_lekopag': float_string(fake, 0, 9999.99),
                    'netunim_nosafim_kahal_maasik_hodshi': float_string(fake, 0, 9999.99),
                    'netunim_nosafim_sahar_lekahal': float_string(fake, 0, 9999.99),

                    'totals_hayav_mh': float_string(fake, 100, 9999.99),
                    'totals_hayav_bl': float_string(fake, 100, 9999.99),
                    'totals_hayav_sahah_tashlumim': float_string(fake, 100, 9999.99),
                    'totals_hayav_sahah_nikuim': float_string(fake, 100, 9999.99),
                    'totals_hayav_sahar_neto': float_string(fake, 100, 9999.99),
                    'totals_hayav_neto_letashlum': float_string(fake, 100, 9999.99),

                    'tashlumim_table': {
                        'div_trs_td_div': get_tashlumim_table(fake)
                    },
                    'nikuy_hova_table': {
                        'div_trs_td_div': [
                            ['מס הכנסה', float_string(fake, 200, 15000)],
                            ['דמי בריאות', float_string(fake, 100, 900)],
                            ['&nbsp;', '&nbsp;'],
                            ['&nbsp;', '&nbsp;'],
                            ['&nbsp;', '&nbsp;'],
                            ['&nbsp;', '&nbsp;'],
                            ['&nbsp;', '&nbsp;'],
                            ['&nbsp;', '&nbsp;'],
                            ['סה"כ', float_string(fake, 800, 30000)],
                        ]
                    },
                    'nikuy_reshut_table': {
                        'div_trs_td_div': get_nikuy_reshut_table(fake)
                    },
                    'headruiot_table': {
                        'div_trs_td_div': [
                            [float_string(fake, 0, 9), str(fake.random_int(0, 9)), float_string(fake, 0, 9)],
                            [float_string(fake, 0, 9), str(fake.random_int(0, 9)), float_string(fake, 0, 9)],
                            [float_string(fake, 0, 9), str(fake.random_int(0, 9)), float_string(fake, 0, 9)],
                        ]
                    },
                    'headruiot_zvira_hofesh': float_string(fake, 0, 9),
                    'headruiot_zvira_mahala': float_string(fake, 0, 9),
                    'headruiot_zvira_havraa': float_string(fake, 0, 9),
                    'headruiot_hodashim_table': {
                        'div_trs_td_div': [
                            get_headruiot_hodashim_row(fake)
                        ]
                    },
                    'netunim_miztabrim_table': {
                        'div_trs_td_div': get_netunim_miztabrim_table(fake)
                    },
                    'footer_production_date': (salary_date + datetime.timedelta(days=fake.random_int(33, 40))).strftime('%d/%m/%Y'),
                    'footer_made_by': '',
                    'footer_made_with': '',
                },
            )
