import datetime
import random
from dateutil.relativedelta import relativedelta

from .salary import Salary

from .. import common_draw, common

BANKS = {
    '11': 'ירושלים',
    '12': 'הפועלים',
    '13': 'לאומי',
    '14': 'דיסקונט',
    '15': 'הבינלאומי',
    '16': 'פאגי',
}

MAR_STATUS = [  # <== it seems that this is the ONLY place in tlush where we have the gender! so the value here does not have to match any other field
    'נשוי',
    'נשואה',
    'רווק',
    'רווקה',
    'גרוש',
    'גרושה',
    'אלמן',
    'אלמנה',
]

PENSIA = [  # <===== ToDo: improve this list. The Ifyun document does not give any list, so I made this up myself
    'מיטב כללית',
    'הראל גילעד',
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
    'קחצ"ק_מניות',
    'קחצ"ק_הראל',
    'ילין לפידות',
    'הפניקס השתלמות כללי',
    'אינפיניטי',
]

def fake_date(fake):
    return fake.date_between(start_date='-3y', end_date='-1y').strftime('%d%m%y')

def random_float(fake, start, end):
    return f'{fake.random_int(100*start, 100*end)/100:,.2f}'

def empty_or(value):
    if random.choice([True, False]):
        return value;
    else:
        return ''

def empty_percent_or(percent, value):
    if random.randint(0, 100) < percent:
        return ''
    else:
        return value

def get_netunim_golmiyim_table(fake, darga_without_tiks):
    res = []
    res.append(['אוכלוסיה', 'קבע', fake_date(fake)])
    res.append(['אחוז תמריץ', '8', fake_date(fake)])   # my suggestion: value should be fake.random_int(8, 15) or similar?
    res.append(['דרגת שכר', darga_without_tiks, fake_date(fake)])
    res.append(['דרוג', 'מנהלי', ''])
    res.append(['ותק בשרות', '02.04.12', fake_date(fake)])
    res.append(['ותק לתוספת ותק', '02.03.00', fake_date(fake)])
    res.append(['יתרת ימי מחלה לניצול', '8', fake_date(fake)])  # my suggestion: value should be fake.random_int(0, 15) or similar?
    res.append(['מצב', 'רגיל', fake_date(fake)])
    res.append(['ניצול שנתי ימי מחלה', '17', fake_date(fake)])  # my suggestion: value should be fake.random_int(0, 15) or similar?
    res.append(['סוג יחידה', 'יח דריכות', ''])
    res.append(['סוג לתוספת מקצועית', '9', fake_date(fake)])    # my suggestion: value should be fake.random_int(7, 25) or similar?


    res.append(['סוג קרן פנסיה', fake.random_element(PENSIA), fake_date(fake)])
    res.append(['שם קרן השתלמות', fake.random_element(HISHTALMUT), fake_date(fake)])
    res.append(['שם קופת גמל שכיר', fake.random_element(GEMEL), fake_date(fake)])

    res.append(['מספר נקודות זיכוי', f'{fake.random_int(100, 500, step=25) / 100:,.2f}', fake_date(fake)])  # 1-5 step 0.25
    res.append(['השתתפות בקופת גמל במ', '10.93', fake_date(fake)])
    res.append(['השתתפות בקרן ההשתלמו', '7.50', fake_date(fake)])
    res.append(['השתתפות בקרן הפנסיה', '728.40', fake_date(fake)])

    res.append(['ברוטו לביטוח לאומי', f'{fake.random_int(1, 3000000)/100:,.2f}', fake_date(fake)])
    res.append(['ברוטו לקופת גמל', f'{fake.random_int(1, 3000000)/100:,.2f}', fake_date(fake)])
    res.append(['ברוטו לפנסיה', f'{fake.random_int(1, 3000000)/100:,.2f}', fake_date(fake)])
    return res

def get_tashlumim_shotfim_table(fake):
    res = []
    res.append(['שכר משולב', empty_percent_or(30, random_float(fake, 1, 3000)), random_float(fake, 1, 3000)])
    descs = set([
        'תוספת הסכם',
        'השלמת משולב',
        'תוספת דריכות',
        'תוספת צבא קבע',
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
    for i in range(fake.random_int(2, 11)):
        if len(descs)==0:
            break
        desc = fake.random_element(list(descs))
        descs.remove(desc)
        res.append([
            desc,
            empty_percent_or(30, random_float(fake, -1000, 3000)),
            empty_percent_or(10, random_float(fake, 1, 3000))
        ])
    for i in range(12-len(res)):
        res.append(['&nbsp;', '&nbsp;', '&nbsp;'])  # <==== ToDo: for some reason the HTML result is not empty (the first field has one blank underlined with blue)
    return res


def get_nikuyim_shotfim_table(fake):
    res = []
    # schum kodem is 30% empty, schum Nochechi 90% has a value
    res.append(['בטוח לאומי', empty_percent_or(30, random_float(fake, 1, 3000)), empty_percent_or(10, random_float(fake, 1, 3000))])
    res.append(['מס הכנסה', empty_percent_or(30, random_float(fake, 1, 3000)), empty_percent_or(10, random_float(fake, 1, 3000))])
    res.append(['ביטוח בריאות ממלכתי', empty_percent_or(30, random_float(fake, 1, 3000)), empty_percent_or(10, random_float(fake, 1, 3000))])
    res.append(['ניכוי לקרן פנסיה', empty_percent_or(30, random_float(fake, 1, 3000)), empty_percent_or(10, random_float(fake, 1, 3000))])
    res.append(['נכוי לקרן השתלמות', empty_percent_or(30, random_float(fake, 1, 3000)), empty_percent_or(10, random_float(fake, 1, 3000))])
    res.append(['ביטוח חיים', empty_percent_or(30, random_float(fake, 1, 3000)), empty_percent_or(10, random_float(fake, 1, 3000))])
    res.append(['השתתפות במצב המשק', empty_percent_or(30, random_float(fake, 1, 3000)), empty_percent_or(10, random_float(fake, 1, 3000))])
    res.append(['חבר משרתי הקבע והגמלאים', empty_percent_or(30, random_float(fake, 1, 3000)), empty_percent_or(10, random_float(fake, 1, 3000))])
    res.append(['כלכלה ביחידה', empty_percent_or(30, random_float(fake, 1, 3000)), empty_percent_or(10, random_float(fake, 1, 3000))])
    res.append(['ביטוח חיים', empty_percent_or(30, random_float(fake, 1, 3000)), empty_percent_or(10, random_float(fake, 1, 3000))])
    return res


class SalarySun(Salary):

    def generate(self):
        fake = self.fake
        darga_with_tiks = fake.random_element(['סמ"ר', 'תא"ל', 'אל"מ', 'סא"ל', 'רס"ן', 'סרן', 'סגן', 'רס"מ', 'רס"ר'])
        darga_without_tiks = darga_with_tiks.replace('"', "") 
        fixed_context = {
            'teudat_zehut': fake.teudat_zehut(),
            'darga': fake.random_element(['סמ"ר', 'תא"ל', 'אל"מ', 'סא"ל', 'רס"ן', 'סרן', 'סגן', 'רס"מ', 'רס"ר']),
            'tom_sherut_date': fake.date_between(start_date='+1y', end_date='+20y').strftime('%d/%m/20%y'),
            'marital_status': fake.random_element(MAR_STATUS),
            
            'bank': BANKS[fake.random_element(list(BANKS.keys()))],
            'bank_branch_code': fake.random_int(90, 999),
            'bank_branch_name': '',
            'bank_account_number': fake.numerify('########'),
            
            'zakaut_shnatit': fake.random_int(1, 30),
            'nizul': fake.random_int(0, 31),
            'yitra_lenizul': fake.random_int(0, 100),
            'yemei_hufsha_zvura': fake.random_int(0, 100),
            'ereh_yom_zvura_bruto': fake.random_int(1, 1000),
            
            'tik_nikuim': fake.numerify("#########"),
            'hahnasa_shnatit_lamas': fake.random_int(1, 300000),
            'hahnasa_zkufa': fake.random_int(1, 300000),
            'hahnasot_lo_socialiot': fake.random_int(1, 300000),
            'hahnasot_had_peamiot': fake.random_int(1, 10000),
            'zikui_shnati_bemas': fake.random_int(1, 10000),
            'ptor_shnati_bemas': fake.random_int(1, 10000),
            'mas_hahnasa': fake.random_int(1, 30000),
            'ahuz_mas_shuli': fake.random_int(10, 50),

            'sahah_tashlumim_shotfim_value': random_float(fake, 1, 30000),
            'sahah_nikuim_shotfim_value': random_float(fake, 1, 30000),
            'sahar_hodshi_neto_value': random_float(fake, 1, 30000),
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
                render_path='salaries/sun.html',
                page=self.html_page,
                http_server_port=self.subtype_context.http_server_port,
                width=2178, height=2922,
                context={
                    **fixed_context,
                    'salary_date': f'{salary_date.month} / {salary_date.year}',
                    'netunim_golmyim_table': {
                        'div_trs_td_div': get_netunim_golmiyim_table(fake, darga_without_tiks)
                    },
                    'tashlumim_table': {
                        'div_trs_td_div': get_tashlumim_shotfim_table(fake)
                    },
                    'nikuyim_table': {
                        'div_trs_td_div': get_nikuyim_shotfim_table(fake)
                    },
                },
            )
