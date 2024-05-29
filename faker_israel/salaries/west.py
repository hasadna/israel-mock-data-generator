import datetime
import random
from dateutil.relativedelta import relativedelta

from .salary import Salary

from .. import common_draw, common

PENSIA = [  # <===== ToDo: improve this list. The Ifyun document does not give any list, so I made this up myself
    'מיטב כללית',
    'כלל פנסיה',
    'הפניקס',
    'מגדל מקפת',
    'מבטחים חדשה',
]
GEMEL = [  # <===== ToDo: improve this list. The Ifyun document does not give any list, so I made this up myself
    'אלטשולר שחם',
    'אנליסט גמל',
    'הפניקס גמל',
    'מגדל לתגמולים ולפיצ',
    'מור מנורה',
]
HISHTALMUT = [  # <===== ToDo: improve this list. The Ifyun document does not give any list, so I made this up myself
    'כלל השתלמות',
    'אלטשולר שחם השתלמות',
    'ילין לפידות',
    'הפניקס השתלמות כללי',
    'אינפיניטי',
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
        return value;
    else:
        return ''

def random_float(fake, start, end):
    return f'{fake.random_int(100*start, 100*end)/100:,.2f}'

def random_float1(fake, start, end):
    return f'{fake.random_int(10*start, 10*end)/10:,.1f}'

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
                empty_or(random_float(fake, -1, 10)),   # range not specified in IFYUN, I made up the numbers
                empty_or(random_float(fake, 0, 1000)),  # range not specified in IFYUN, I made up the numbers
                empty_or(random_float(fake, 0, 1000)),  # range not specified in IFYUN, I made up the numbers
                empty_or(random_float(fake, 0, 1000)),  # range not specified in IFYUN, I made up the numbers
                empty_or(random_float(fake, 0, 3000))   # range not specified in IFYUN, I made up the numbers # Ifyun says it could be empty!
                ])
    for i in range(12-len(res)):
        res.append(['&nbsp;', '&nbsp;', '&nbsp;', '&nbsp;', '&nbsp;', '&nbsp;', '&nbsp;'])
    return res


def get_nikuyim_table(fake):
    res = []
    res.append(['&nbsp;', 'ב. לאומי',  random_float(fake, 1, 3000)])    # range not specified in IFYUN, I made up the numbers
    res.append(['&nbsp;', 'מס הכנסה',  random_float(fake, 1, 3000)])    # range not specified in IFYUN, I made up the numbers
    res.append(['&nbsp;', 'מס בריאות',  random_float(fake, 1, 3000)])   # range not specified in IFYUN, I made up the numbers
    res.append([a_3_digits_code(fake), truncate(fake.random_element(PENSIA), 13), random_float(fake, 1, 3000)])   # range not specified in IFYUN, I made up the numbers
    if fake.random_int(0, 100) < 10:
        res.append([a_3_digits_code(fake), truncate(fake.random_element(HISHTALMUT), 13), random_float(fake, 1, 3000)])
    if fake.random_int(0, 100) < 10:
        res.append([a_3_digits_code(fake), truncate(fake.random_element(HISHTALMUT), 13), random_float(fake, 1, 3000)])
    if fake.random_int(0, 100) < 10:
        res.append([a_3_digits_code(fake), truncate(fake.random_element(GEMEL), 13), random_float(fake, 1, 3000)])
    if fake.random_int(0, 100) < 10:
        res.append([a_3_digits_code(fake), truncate(fake.random_element(GEMEL), 13), random_float(fake, 1, 3000)])
    for i in range(8-len(res)):
        res.append(['&nbsp;', '&nbsp;', '&nbsp;'])
    return res


def get_nikuyim_optional_table(fake):
    res = []
    descs = set([
        'קו הבריאות',
        'תשלומים לעיריה',
        'ביטוח שיניים',
        'החזרי הלוואות',
        'השתתפות בקורס',
    ])
    for i in range(fake.random_int(0, 5)): # IFYUN does not say how many lines should be in table. I decided 0-5
        if len(descs)==0:
            break
        desc = fake.random_element(list(descs))
        descs.remove(desc)
        res.append([a_3_digits_code(fake), 
                desc, # from list
                empty_or(random_float(fake, -1000, 3000))])   # IFYUN does not say the sum of nikuy. I decided -1000 to 3000 
                                                            # IFYUN specifically says sum could be empty
    for i in range(5-len(res)):     # IFYUN does not say how many lines should be in table. I decided 5
        res.append(['&nbsp;', '&nbsp;', '&nbsp;'])
    return res


def get_aggregate_table(fake):
    res = []
    res.append(['שכר חייב מס',  random_float(fake, 1, 3000)])    # range not specified in IFYUN, I made up the numbers
    res.append(['שווי למס',  random_float(fake, 1, 3000)])    # range not specified in IFYUN, I made up the numbers
    res.append(['שכ.ב.לאומי',  random_float(fake, 1, 3000)])    # range not specified in IFYUN, I made up the numbers
    res.append(['בט. לאומי',  random_float(fake, 1, 3000)])    # range not specified in IFYUN, I made up the numbers
    res.append(['מס הכנסה',  random_float(fake, 1, 3000)])    # range not specified in IFYUN, I made up the numbers
    res.append(['מס בריאות',  random_float(fake, 1, 3000)])    # range not specified in IFYUN, I made up the numbers
    res.append([truncate(fake.random_element(PENSIA), 13), random_float(fake, 1, 3000)])   # range not specified in IFYUN, I made up the numbers
    if fake.random_int(0, 100) < 50:
        res.append([truncate(fake.random_element(HISHTALMUT), 13), random_float(fake, 1, 3000)])
    if fake.random_int(0, 100) < 10:
        res.append([truncate(fake.random_element(HISHTALMUT), 13), random_float(fake, 1, 3000)])
    if fake.random_int(0, 100) < 10:
        res.append([truncate(fake.random_element(GEMEL), 13), random_float(fake, 1, 3000)])
    if fake.random_int(0, 100) < 10:
        res.append([truncate(fake.random_element(GEMEL), 13), random_float(fake, 1, 3000)])
    for i in range(11-len(res)):
        res.append(['&nbsp;', '&nbsp;'])
    return res


def get_vacation_table(fake):
    res = []
    # Note - we don't generate a value for the first column because it is already displayed in the template and is always the same!
    res.append(['',  random_float(fake, 0, 30)])    # range not specified in IFYUN, I made up the numbers
    res.append(['',  random_float(fake, 1, 3)])    # range not specified in IFYUN, I made up the numbers
    res.append(['',  random_float(fake, 0, 10)])    # range not specified in IFYUN, I made up the numbers
    res.append(['',  random_float(fake, 0, 30)])    # range not specified in IFYUN, I made up the numbers
    return res


def get_sick_table(fake):
    res = []
    # Note - we don't generate a value for the first column because it is already displayed in the template and is always the same!
    res.append(['',  random_float(fake, 0, 30)])    # range not specified in IFYUN, I made up the numbers
    res.append(['',  random_float(fake, 1, 3)])    # range not specified in IFYUN, I made up the numbers
    res.append(['',  random_float(fake, 0, 10)])    # range not specified in IFYUN, I made up the numbers
    res.append(['',  random_float(fake, 0, 30)])    # range not specified in IFYUN, I made up the numbers
    return res


def get_other_data_table1(fake):
    res = []
    # Note - we don't generate a value for the first column because it is already displayed in the template and is always the same!
    res.append(['',  fake.random_int(0, 31)]) 
    res.append(['', random_float1(fake, 0, 250)])
    res.append(['',  fake.random_int(0, 200)]) 
    res.append(['', random_float(fake, 0.5, 15)])
    res.append(['', random_float(fake, 2, 12)])
    # <=== אחוז מס שולי - IFYUN says nothing about that line
    # <=== next 3 lines, IFYUN says קבוע - I don't know what it means, currently these lines always as in template (same values in all generated slips)
    return res


def get_other_data_table2(fake):
    res = []
    res.append(['',  fake.random_int(0, 31)]) 
    res.append(['', random_float1(fake, 0, 250)])
    # <=== following fields IFYUN says לרנדר מספר כפי שבוצע בתלושים קודמים I don't know exactly what values they mean by that
    res.append(['', random_float(fake, 1, 3000)]) # I made up the values because IFYUN doesn't specify
    res.append(['', random_float(fake, 1, 3000)]) # I made up the values because IFYUN doesn't specify
    res.append(['', random_float(fake, 1, 3000)]) # I made up the values because IFYUN doesn't specify
    res.append(['', random_float(fake, 1, 3000)]) # I made up the values because IFYUN doesn't specify
    res.append(['', random_float(fake, 1, 3000)]) # I made up the values because IFYUN doesn't specify
    res.append(['', random_float(fake, 1, 3000)]) # I made up the values because IFYUN doesn't specify
    res.append(['', random_float(fake, 1, 3000)]) # I made up the values because IFYUN doesn't specify
    res.append(['', random_float(fake, 1, 3000)]) # I made up the values because IFYUN doesn't specify
    res.append(['', random_float(fake, 1, 3000)]) # I made up the values because IFYUN doesn't specify
    res.append(['', random_float(fake, 1, 3000)]) # I made up the values because IFYUN doesn't specify
    return res


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
            #'department': '',  # <========= ToDo: implement this
            'job_start': fake.date_between(start_date='-30y', end_date='-5y').strftime('%d/%m/%Y'), # <=== %Y is 4 digit year
            #'family_status': '',   # <========= ToDo: implement this
            'derug': pad_with_zeros(fake.random_int(0, 999),3),
            'darga': pad_with_zeros(fake.random_int(0, 999),3),
            'vetek_from': empty_or(fake.date_between(start_date='-30y', end_date='-5y').strftime('%d/%m/%Y')),
            'bank': str(bank_num) + '/' + str(fake.random_int(90, 999)),
            'account': fake.numerify('#######'),    

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
                    'printed_at': f'10/{1+salary_date.month}/{salary_date.year}',

                    'tashlumim_table': {
                        'div_trs_td_div': get_tashlumim_table(fake)
                    },
                    'shovi_mas': random_float(fake, 0, 1000),       # <=== IFYUN did not specify the range, I made up 0-1000
                    'tashlum_total': random_float(fake, 0, 30000),  # <=== IFYUN did not specify the range, I made up 0-30000

                    'nikuyim_table': {
                        'div_trs_td_div': get_nikuyim_table(fake)
                    },
                    'mandatory_nikuy': random_float(fake, 0, 3000),    # <=== IFYUN did not specify the range, I made up 0-3000

                    'nikuyim_optional_table': {
                        'div_trs_td_div': get_nikuyim_optional_table(fake)
                    },
                    'nikuyim_total': random_float(fake, -1000, 3000),    # <=== IFYUN did not specify the range, I made up -1000 - 3000,

                    'salary_neto': random_float(fake, 0, 30000),  # <=== IFYUN did not specify the range, I made up 0-30000,
                    'aggregate_table': {
                        'div_trs_td_div': get_aggregate_table(fake)
                    },
                    'vacation_table': {
                        'div_trs_td_div': get_vacation_table(fake)
                    },
                    'sick_table': {
                        'div_trs_td_div': get_sick_table(fake)
                    },
                    'other_data_table1': {
                        'div_trs_td_div': get_other_data_table1(fake)
                    },
                    'other_data_table2': {
                        'div_trs_td_div': get_other_data_table2(fake)
                    },
                    'tashlum': random_float(fake, 0, 30000),  # <=== IFYUN did not specify this field AT ALL, I added and made up 0-30000,
                },
            )
