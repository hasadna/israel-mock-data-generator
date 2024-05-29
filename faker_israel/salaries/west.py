import datetime
import random
from dateutil.relativedelta import relativedelta

from .salary import Salary

from .. import common_draw, common
from . import north


GEMEL = [
    'מיטב כללית',
    'כלל פנסיה',
    'הפניקס',
    'מגדל מקפת',
    'מבטחים חדשה',
    'אלטשולר שחם',
    'אנליסט גמל',
    'הפניקס גמל',
    'מגדל לתגמולים ולפיצ',
    'מור מנורה',
    'כלל השתלמות',
    'אלטשולר שחם השתלמות',
    'ילין לפידות',
    'הפניקס השתלמות כללי',
    'אינפיניטי',
]


NIKUYIM_RESHUT = [
    'קו הבריאות',
    'תשלומים לעירייה',
    'ביטוח שיניים',
    'החזרי הלוואות',
    'השתתפות בקורס',
]


def pad_with_zeros(value, total_char_num):
    val = str(value)
    if len(val) < total_char_num:
        new_val = ((total_char_num - len(val)) * '0') + val
        return new_val
    else:
        return val

def empty_or(value):
    if random.choice([True, False]):
        if not value:
            return '&nbsp;'
        else:
            return value
    else:
        return '&nbsp;'

def random_float(fake, start, end):
    return f'{fake.random_int(100*start, 100*end)/100:,.2f}'

def a_3_digits_code(fake):
    return pad_with_zeros(fake.random_int(1, 999),3)

def truncate(str_val, max_char_num):
    if len(str_val) <= max_char_num:
        return str_val
    else:
        return str_val[:max_char_num]


def get_tashlumim_table(fake):
    res = []
    descs = set([
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
        'ביגוד',
        'הוצאות אחרות',
    ])
    for i in range(fake.random_int(3, 12)):
        if len(descs)==0:
            break
        desc = fake.random_element(list(descs))
        descs.remove(desc)
        res.append([a_3_digits_code(fake), 
                desc, # from list
                empty_or(random_float(fake, -1, 10)),
                empty_or(random_float(fake, 0, 30000)),
                empty_or(random_float(fake, 0, 1000)),
                empty_or(random_float(fake, 0, 1500)),
                empty_or(random_float(fake, 0, 10000))
                ])
    for i in range(12-len(res)):
        res.append(['&nbsp;', '&nbsp;', '&nbsp;', '&nbsp;', '&nbsp;', '&nbsp;', '&nbsp;'])
    return res


def get_nikuyim_table(fake):
    res = [
        ['&nbsp;', 'ב. לאומי', random_float(fake, 1, 3000)],
        ['&nbsp;', 'מס הכנסה', random_float(fake, 1, 3000)],
        ['&nbsp;', 'מס בריאות', random_float(fake, 1, 3000)]
    ]
    gemel = set(GEMEL)
    for i in range(fake.random_int(1, 5)):
        g = fake.random_element(list(gemel))
        gemel.remove(g)
        res.append([a_3_digits_code(fake), g, empty_or(random_float(fake, 1, 3000))])
    for i in range(8-len(res)):
        res.append(['&nbsp;', '&nbsp;', '&nbsp;'])
    return res


def get_nikuyim_optional_table(fake):
    nikuyim = set(NIKUYIM_RESHUT)
    res = []
    for i in range(fake.random_int(0, 3)):
        nikuy = fake.random_element(list(nikuyim))
        nikuyim.remove(nikuy)
        res.append([a_3_digits_code(fake), nikuy, empty_or(random_float(fake, 1, 3000))])
    for i in range(5-len(res)):
        res.append(['&nbsp;', '&nbsp;', '&nbsp;'])
    return res


def get_aggregate_table(fake):
    res = [
        ['שכר חייב מס', random_float(fake, 1000, 5000)],
        ['שווי למס', random_float(fake, 1000, 5000)],
        ['שכ.ב.לאומי', random_float(fake, 1000, 5000)],
        ['בט.לאומי', random_float(fake, 1000, 5000)],
        ['מס הכנסה', random_float(fake, 1000, 5000)],
        ['מס בריאות', random_float(fake, 1000, 5000)],
    ]
    gemels = set(GEMEL)
    for i in range(fake.random_int(1, 5)):
        gemel = fake.random_element(list(gemels))
        gemels.remove(gemel)
        res.append([gemel, random_float(fake, 1000, 5000)])
    for i in range(11-len(res)):
        res.append(['&nbsp;', '&nbsp;'])
    return res


def get_family_status(fake):
    status = fake.random_element(['נ', 'ר', 'ג', 'א'])
    kids = 0
    if fake.random_int(0, 2) == 2:
        kids = fake.random_int(0, 19)
    status += '+' + str(kids)
    return status


class SalaryWest(Salary):

    def generate(self):
        fake = self.fake

        tik_nikuyim_value = fake.numerify("#########")
        tik_bil_value = tik_nikuyim_value + '00'
        bank_name = fake.random_element(common.BANKS_NUMBERS.keys())
        bank_num = common.BANKS_NUMBERS[bank_name]

        fixed_context = {
            'company_name': fake.company(),
            'company_address': f'{fake.street_address()}',
            'company_address_city': f'{fake.city()}, {fake.postcode()}',
            'tik_nikuyim': tik_nikuyim_value,
            'company_number': fake.numerify("#########"),
            'tik_bil': tik_bil_value,

            'employee_name': fake.first_name() + ' ' + fake.last_name(),
            'employee_address': f'{fake.street_address()}',   
            'employee_address_city': f'{fake.city()}, {fake.postcode()}',

            'id_number': fake.teudat_zehut(),
            'employee_number': fake.random_int(1, 9999),
            #'misra_sameh': '', # use default that is in template
            'misra_bil': fake.random_element(['עיקרית','מישנית']),
            'toshav': fake.random_element(['כן','לא']),
            'salary_base': fake.random_element(['חודשי','שעתי']),
            'part_job': f'{fake.random_int(10, 100, step=10) / 100:,.1f}' + '000',
            'vetek': fake.date_between(start_date='-30y', end_date='-5y').strftime('%d.%m.%y'),
            'department': fake.random_element(north.MAHLAKOT) + f' 0{fake.random_int(1, 99):02d}',
            'job_start': fake.date_between(start_date='-30y', end_date='-5y').strftime('%d/%m/%Y'), # <=== %Y is 4 digit year
            'family_status': get_family_status(fake),
            'derug': pad_with_zeros(fake.random_int(0, 999),3),
            'darga': pad_with_zeros(fake.random_int(0, 999),3),
            'vetek_from': empty_or(fake.date_between(start_date='-30y', end_date='-5y').strftime('%d/%m/%Y')),
            'bank': str(bank_num) + '/' + str(fake.random_int(90, 999)),
            'account': fake.numerify('#######'),    

            'shovi_mas': random_float(fake, 500, 1500),
            'tashlum_total': random_float(fake, 1000, 30000),
            
            'mandatory_nikuy': random_float(fake, 1000, 3000),

            'nikuyim_total': random_float(fake, -1000, 3000),

            'salary_neto': random_float(fake, 1000, 30000),
            'tashlum': random_float(fake, 500, 30000),
        }
        first_year = fake.random_int(2012, 2022)
        first_month = fake.random_int(1, 10)
        first_date = datetime.date(first_year, first_month, 1)
        for salary_date_num, salary_date in enumerate([
            first_date,
            first_date + relativedelta(months=1),
            first_date + relativedelta(months=2),
        ]):
            printer_at_date = salary_date + relativedelta(months=1)
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
                    'printed_at': f'10/{printer_at_date.month}/{printer_at_date.year}',

                    'tashlumim_table': {
                        'div_trs_td_div': get_tashlumim_table(fake)
                    },
                    'nikuyim_table': {
                        'div_trs_td_div': get_nikuyim_table(fake)
                    },
                    'nikuyim_optional_table': {
                        'div_trs_td_div': get_nikuyim_optional_table(fake)
                    },
                    'aggregate_table': {
                        'div_trs_td_div': get_aggregate_table(fake)
                    },
                    'vacation_kodemet': random_float(fake, 0, 99),
                    'vacation_zvira': random_float(fake, 0, 99),
                    'vacation_nizul': random_float(fake, 0, 99),
                    'vacation_hadasha': random_float(fake, 0, 99),
                    'sick_kodemet': random_float(fake, 0, 99),
                    'sick_zvira': random_float(fake, 0, 99),
                    'sick_nizul': random_float(fake, 0, 99),
                    'sick_hadasha': random_float(fake, 0, 99),
                    'od_yemey_avoda': fake.random_int(0, 31),
                    'od_shot_avoda': f'{fake.random_int(0, 2500)/10:,.1f}',
                    'od_headrut': fake.random_int(0, 200),
                    'od_shot_leyom': f'{fake.random_int(50, 1500)/100:,.2f}',
                    'od_nekudot_regilot': f'{fake.random_int(200, 1200)/100:,.2f}',
                    # 'od_mas_shuli': '',
                    # 'od_kod_mahadora': '',
                    # 'od_hishuv_miztaber': '',
                    # 'od_ofen_tashlum': '',
                    'od2_yaa_bahevra': fake.random_int(0, 31),
                    'od2_yasha_bahevra': f'{fake.random_int(0, 2500)/10:,.1f}',
                    'od2_sahar_hayav_mas': f'{fake.random_int(50000, 500000)/100:,.2f}',
                    'od2_sahar_bituach_leumi': f'{fake.random_int(50000, 500000)/100:,.2f}',
                    'od2_sahar_mevutach': f'{fake.random_int(50000, 500000)/100:,.2f}',
                    'od2_basis_karhash': f'{fake.random_int(50000, 500000)/100:,.2f}',
                    'od2_gemel_maasik': f'{fake.random_int(50000, 500000)/100:,.2f}',
                    'od2_karhash_maasik': f'{fake.random_int(50000, 500000)/100:,.2f}',
                    'os2_lafiz': f'{fake.random_int(50000, 500000)/100:,.2f}',
                    'od2_bituach_leumi_maasik': f'{fake.random_int(50000, 500000)/100:,.2f}',
                    # 'od2_sahar_min_hodshi': f'{fake.random_int(50000, 500000)/100:,.2f}',
                    # 'od2_sahar_min_shaa': f'{fake.random_int(50000, 500000)/100:,.2f}',
                },
            )
