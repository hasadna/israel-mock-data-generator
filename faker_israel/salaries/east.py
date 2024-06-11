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

def get_netunim_miztabrim_table(fake):
    res = []
    res.append([random_float(fake, 1, 999999)])      # ברוטו רגיל   
    res.append([random_float(fake, 1, 999999)])      # ברוטו לא קבוע   
    res.append([random_float(fake, 1, 999999)])      # ברוטו שנים קודמות   
    res.append([random_float(fake, 1, 999999)])      # שווי למס   
    res.append([random_float(fake, 1, 999999)])      # נטו לגילום   
    res.append([random_float(fake, 1, 999999)])      # גילום מס   
    res.append([random_float(fake, 1, 999999)])      # גילום ב.ל   
    res.append([random_float(fake, 1, 999999)])      # מס רגיל   
    res.append([random_float(fake, 1, 999999)])      # מס על ברוטו לא קבוע   
    res.append([random_float(fake, 1, 999999)])      # מס שנים קודמות   
    res.append([random_float(fake, 1, 999999)])      # הכנסה לא מבוטחת   
    res.append([random_float(fake, 1, 999999)])      # ניכוי לסעיף 45א   
    res.append([fake.random_int(100, 300)])          # ערך נקודות זיכוי   
    res.append([random_float(fake, 1, 999999)])      # הכנסה חייבת במס   
    res.append([random_float(fake, 1, 999999)])      # שכר חייב ב.ל   
    return res

def get_yechidot_mas_table(fake):
    res = []
    # three '25' and one '' means 25% of values will be empty
    #  - my decision (not specified in IFYUN how many should be empty)
    for i in range(1, 12):
        res.append([fake.random_element(['25','25','25',''])]) 
    return res


# I think 2 of the values specified in the IFYUN are too long:
# 'נקודות זיכוי ממס הכנסה להורה לילד' and 'נקודות זיכוי ממס הכנסה בגין תואר שלישי במסלול ישיר'
def get_peirut_nekudot_zikuy_table(fake):
    res = []
    res.append([fake.random_element(['תושב ישראל','תושבת ישראל']), # male or female - this is not synchronized with the person first name!
                f'{fake.random_int(100, 500, step=25) / 100:,.2f}'])    # 1-5 step 0.25
    # 2nd row only in 50% of salaries
    if (fake.random_element(['y','n']) == 'y'):
        res.append([fake.random_element(['נקודות זיכוי ממס הכנסה להורה לילד', 'נוער עובד',
                                         'נקודות זיכוי ממס הכנסה בגין תואר שלישי במסלול ישיר','עובדים זרים','מזונות']), 
                    f'{fake.random_int(100, 500, step=25) / 100:,.2f}'])    # 1-5 step 0.25
    return res


def get_netunim_nosafim_haganat_hasachar_table(fake):
    res = []
    # exactly 8 rows
    res.append(['התקופה בעדה בוצע ניתוח נוכחות מ' + f'{fake_date(fake)}' + 'עד ' + f'{fake_date(fake)}'])
    # in following line XX and Y not specified in IFYUN, I made up values as I think necessary
    res.append(['בתקופה ניתוח הנוכחות נדרשו ' + f'{fake.random_int(1, 30)}' + ' ימי עבודה בהם ' + f'{random_float(fake, 100, 200)}' + ' שעות תקן'])
    # in following line XX and Y not specified in IFYUN, I made up values as I think necessary
    res.append(['בתקופה ניתוח הנוכחות בוצעו בפועל ' + f'{fake.random_int(1, 30)}' + ' ימי עבודה ובהם ' + f'{random_float(fake, 100, 200)}' + ' שעות'])
    # in following line X and Y not specified in IFYUN, I made up values as I think necessary
    res.append(['ותק אצל המעסיק ' + f'{fake.random_int(1, 20)}' + ' שנים ו ' + f'{fake.random_int(1, 11)}' + ' חודשים'])
    res.append(['שכר לקצבה ' + f'{random_float(fake, 1, 99999)}' + ' שכר לביטוח אובדן כושר עבודה ' + f'{random_float(fake, 1, 99999)}'])
    res.append(['שכר לקרן השתלמות ' + f'{random_float(fake, 1, 99999)}'])
    res.append(['סך כל הניכויים ' + f'{random_float(fake, 1, 99999)}' + 'ש"ח'])
    res.append(['שכר מינימום לחודש 5880.02 לשעה 31.62'])
    return res

def get_netunim_nosafim_table(fake, tz_number):
    res = []
    # it has 3 parts, I'm not sure all of them are in the same div_trs_td_div ???
    # part 1 netunim ishiyim
    res.append([tz_number])
    res.append([fake.random_element(['רווק','גרוש', 'נשוי', 'אלמן'])])
    res.append([fake.random_int(0, 12)])
    res.append([fake.random_element(['מאוחדת','כללית', 'לאומית', 'מכבי'])])
    res.append([fake.random_element(['הסתדרות כללית','הסתדרות החדשה', 'לא חבר'])])
    res.append([fake.random_element(['רגיל','נכות', 'פנסיונר', 'סטודנט'])])
    res.append(['מס חודשי מצטבר'])
    # part 2 netuney haasaka
    res.append([fake_date(fake)])
    res.append([fake.random_element(['חודשי','חודשי ק.מחופש', 'יומי', 'שבועי'])])
    res.append([f'{fake.random_int(10, 100)}' + '%'])
    res.append([f'{fake.random_int(10, 500, step=5) / 10:,.1f}' + "ש.שבוע' " + f'{fake.random_int(10, 200)}'])
    res.append([f'{fake.random_int(10, 500, step=5) / 10:,.1f}' + " שעות שבועי"])
    # part 3 netunim chodshiyim
    res.append([random_float(fake, 1, 99999)])
    res.append([random_float(fake, 1, 99999)])
    res.append([random_float(fake, 1, 99999)])  # not specified in IFYUN, I decided same as row above
    res.append([f'{fake.random_int(0, 50)}' + '%'])
    res.append([f'{fake.random_int(200, 1200, step=25) / 100:,.2f}'])   # 2-12 step 0.25
    res.append([random_float(fake, 1, 99999)])
    res.append([random_float(fake, 1, 99999)])
    return res


def get_ishurei_pkid_shuma_table(fake):
    res = []
    # exactly 1 row
    res.append([f'{fake_date(fake)}', 
                f'{fake_date(fake)}',
                fake.random_element(['1 נקודות זיכוי למשפחה חד הורית/מזונות לילדים', 
                                     'שיעור מס נתון 20% עד ל14110 ש"ח ושיעור מס 31% מעליו',
                                         'זכאי לתקרות קופות גמל על פי החוק'])])
    return res


def get_hodaa_laoved_table(fake):
    res = []
    res.append(['שעות העבודה מתייחסות לחודש הקודם'])
    res.append(['***'])
    res.append(['מנהל/ת אגף:'])
    # add 2 lines here, not specified in IFYUN how to fake
    res.append([''])
    res.append(['מנהל/ת מש"א:'])
    # add 2 lines here, not specified in IFYUN how to fake
    res.append([''])
    res.append(['רפרנטית נוכחות:'])
    # add 2 lines here, not specified in IFYUN how to fake
    res.append([''])
    res.append(['מנהל/ת מש"א:'])
    res.append([''])
    res.append(['חשבת שכר:'])
    # add 2 lines here, not specified in IFYUN how to fake
    res.append([''])
    res.append(['*'])
    res.append(['סוכנות הביטוח המטפלת בתיק שלך : ' + ''])   # add name of sochnut, not specified in IFYUN how to fake
    res.append(['מצ"ב פרטי ההתקשרות עמם :'])    
    res.append([''])    # add 1 line value here, not specified in IFYUN how to fake
    return res

def random_float(fake, start, end):
    return f'{fake.random_int(100*start, 100*end)/100:,.2f}'


def fake_date(fake):
    return fake.date_between(start_date='-3y', end_date='-1y').strftime('%d/%m/%y')


class SalaryEast(Salary):


    def generate(self):
        fake = self.fake
        machlaka_number = fake.random_int(50, 99999)
        tz_number = fake.teudat_zehut()
        fixed_context = {
            'teudat_zehut': tz_number,
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

            # not specified in IFYUN but I think this table must be in fixed_context
            'netunim_nosafim_table': {
                'div_trs_td_div': get_netunim_nosafim_table(fake, tz_number)
            },
            # not specified in IFYUN but I think this table must be in fixed_context
            'hodaa_laoved_table': {
                'div_trs_td_div': get_hodaa_laoved_table(fake)
            },
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


                    'netunim_miztabrim_table': {
                        'div_trs_td_div': get_netunim_miztabrim_table(fake)
                    },
                    'yechidot_mas_table': { # need to make sure. possibly this table not the usual div tr td div??
                        'div_trs_td_div': get_yechidot_mas_table(fake)
                    },
                    'peirut_nekudot_zikuy_table': {
                        'div_trs_td_div': get_peirut_nekudot_zikuy_table(fake)
                    },
                    'netunim_nosafim_haganat_hasachar_table': {
                        'div_trs_td_div': get_netunim_nosafim_haganat_hasachar_table(fake)
                    },
                    'ishurei_pkid_shuma_table': {
                        'div_trs_td_div': get_ishurei_pkid_shuma_table(fake)
                    },

                },
            )
