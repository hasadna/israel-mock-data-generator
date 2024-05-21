import datetime
from dateutil.relativedelta import relativedelta

from .salary import Salary

from .. import common_draw, common, educational_institues


BANKS = {
    '11': 'ירושלים',
    '12': 'הפועלים',
    '13': 'לאומי',
    '14': 'דיסקונט',
    '15': 'הבינלאומי',
    '16': 'פאגי',
}


DARGOT = [
    '',
    'תואר ראשון',
    'תואר שני',
    'תואר שלישי'
]


MAR_STATUS = [
    'נשוי',
    'נשואה',
    'רווק',
    'רווקה',
    'גרוש',
    'גרושה',
    'אלמן',
    'אלמנה',
]


TASHLUMS_STATIC = [
    'תוספת באחוזים',
    'תוספת ע"פ חוק',
]
TASHLUMS_WITH_YEARS = [
    'הסכם שכר',
    'תוספת',
    'תוספת שקלית',
    'תוספת אחוזים',
]


def get_tashlumim_table(fake):
    res = []
    tashlums = set(TASHLUMS_STATIC)
    for tashlum in TASHLUMS_WITH_YEARS:
        for i in range(4):
            tashlums.add(f'{tashlum} {fake.random_int(1990, 2022)}')
    for i in range(fake.random_int(4, 11)):
        if i == 3:
            res.append([
                '&nbsp;', '&nbsp;', '&nbsp;', '&nbsp;', '&nbsp;', '&nbsp;',
                'סה"כ אופק חדש', '&nbsp;',
                f'{fake.random_int(300000, 1500000) / 100:,.2f}'
            ])
        else:
            tashlum = fake.random_element(list(tashlums))
            tashlums.remove(tashlum)
            res.append([
                f'{fake.random_int(1, 1000):,.2f}' if fake.random_int(1, 2) == 1 else '',
                f'{fake.random_int(1, 100):,.2f}' if fake.random_int(1, 2) == 1 else '',
                f'{fake.random_int(1, 12):02d}/{fake.random_int(1990, 2022)}' if fake.random_int(1, 2) == 1 else '',
                f'{fake.random_int(1, 12):02d}/{fake.random_int(1990, 2022)}' if fake.random_int(1, 2) == 1 else '',
                fake.random_int(1, 999),
                f'{fake.random_int(10, 1000)/10:,.1f}%' if fake.random_int(1, 2) == 1 else '',
                tashlum,
                f'{fake.random_int(150, 3000) * fake.random_element([-1, 1]):,.2f}',
                f'{fake.random_int(300000, 1500000) / 100:,.2f}',
            ])
    for i in range(17-len(res)):
        res.append(['&nbsp;', '&nbsp;', '&nbsp;', '&nbsp;', '&nbsp;', '&nbsp;', '&nbsp;', '&nbsp;', '&nbsp;'])
    return res


KUPOT_GEMEL = [
    'ועד סגל סוטר',
    'קו הבריאות',
    'תשלומים לעירייה',
    'ביטוח שיניים',
    'החזרי הלוואות',
    'השתתפות בקורס',
    'אלטשולר',
    'מבטחים חדשה',
    'חרב גמל',
    'הסתדרות המורים',
]


def get_nikuey_gemel_table(fake):
    res = []
    kupot = set(KUPOT_GEMEL)
    for i in range(fake.random_int(3, 10)):
        kupa = fake.random_element(list(kupot))
        kupot.remove(kupa)
        res.append([
            kupa,
            f'{fake.random_int(1, 12):02d}/{fake.random_int(1990, 2022)}' if fake.random_int(1, 2) == 1 else '',
            f'{fake.random_int(1, 12):02d}/{fake.random_int(1990, 2022)}' if fake.random_int(1, 2) == 1 else '',
            fake.numerify('#######') if fake.random_int(1, 2) == 1 else '',
            f'{fake.random_int(100, 3000000)/100:,.2f}' if fake.random_int(1, 2) == 1 else '',
            f'{fake.random_int(0, 100000)/100:,.2f}' if fake.random_int(1, 2) == 1 else '',
            f'{fake.random_int(0, 100000)/100:,.2f}' if fake.random_int(1, 2) == 1 else '',
            f'{fake.random_int(0, 100000)/100:,.2f}' if fake.random_int(1, 2) == 1 else '',
        ])
    for i in range(11-len(res)):
        res.append(['&nbsp;', '&nbsp;', '&nbsp;', '&nbsp;', '&nbsp;', '&nbsp;', '&nbsp;', '&nbsp;'])
    return res


def get_nikuyim_aherim_table(fake):
    res = []
    descs = set([
        'קו הבריאות',
        'תשלומים לעירייה',
        'ביטוח שיניים',
        'החזרי הלוואות',
        'השתתפות בקורס',
    ])
    for i in range(fake.random_int(3, 5)):
        desc = fake.random_element(list(descs))
        descs.remove(desc)
        res.append([
            f'{fake.random_int(1, 999):02d}',
            desc,
            f'{fake.random_int(1, 100000) / 100:,.2f}' if fake.random_int(1, 2) == 1 else '',
            f'{fake.random_int(1, 100000) / 100:,.2f}' if fake.random_int(1, 2) == 1 else '',
            f'{fake.random_int(1, 100000) / 100:,.2f}' if fake.random_int(1, 2) == 1 else '',
        ])
    for i in range(12-len(res)):
        res.append(['&nbsp;', '&nbsp;', '&nbsp;', '&nbsp;', '&nbsp;'])
    return res


class SalaryCenter(Salary):

    def generate(self):
        fake = self.fake
        first_name = fake.first_name()
        last_name = fake.last_name()
        tik_nikuim = fake.numerify("#########")
        bank_number = fake.random_element(list(BANKS.keys()))
        bank_name = BANKS[bank_number]
        date_of_birth = fake.date_between(start_date='-60y', end_date='-25y')
        fixed_context = {
            'top_name': f'{first_name} {last_name}',
            'top_address': f'{fake.street_address()}',
            'top_city_zip': f'{fake.city()}, {fake.postcode()}',
            'top_semel_mosad': fake.numerify('######'),
            'top_mosad_name': fake.random_element(educational_institues.get_education_institues_set()),
            'top_tiknikuim_mashachnasa': tik_nikuim,
            'top_tiknikuim_bituah_leumi': f'{tik_nikuim}00',
            'top_hashav_sahar': fake.name(),
            'top_pakid': fake.name(),
            'top_hashav_phone': fake.numerify('073#######'),
            'top_employee_address': f'{fake.street_address()} ירושלים',
            'personal_details_teudat_zehut': fake.teudat_zehut(),
            'personal_details_first_name': first_name,
            'personal_details_last_name': last_name,
            'personal_details_bank': f'{bank_number} - {bank_name}',
            'personal_details_snif': f'{fake.numerify("###")} - {fake.city()}',
            'personal_details_heshbon': fake.numerify('#######'),
            'personal_details_darga': fake.random_element(DARGOT),
            'personal_Details_derug_ofek': fake.random_element(DARGOT),
            'personal_details_darga_ofek': fake.random_int(1, 10) if fake.random_int(1, 3) != 1 else '',
            'personal_details_vetek_horaa': fake.random_int(10, 30) if fake.random_int(1, 2) == 1 else '',
            'personal_details_vetek_benihul': fake.random_int(10, 30) if fake.random_int(1, 2) == 1 else '',
            'personal_details_vetek_beyeutz': fake.random_int(10, 30) if fake.random_int(1, 2) == 1 else '',
            'personal_details_vetek_behadracha': fake.random_int(10, 30) if fake.random_int(1, 2) == 1 else '',
            'personal_details_vetek_bezahal': fake.random_int(10, 30) if fake.random_int(1, 2) == 1 else '',
            'personal_details_vetek_beofek': fake.random_int(10, 30) if fake.random_int(1, 2) == 1 else '',
            'personal_Details_work_start_date': fake.date_between(start_date=date_of_birth + datetime.timedelta(days=365*20), end_date='-2y').strftime('%d/%m/%Y'),
            'netuney_mas_marstatus': fake.random_element(MAR_STATUS),
            'netuney_mas_points_kids': f'{fake.random_int(100, 300) / 100:,.2f}' if fake.random_int(1, 3) != 1 else '',
            'netuney_mas_points': f'{fake.random_int(100, 700, step=25) / 100:,.2f}',
            'netuney_mas_percent_mas': f'{fake.random_int(10, 50):,.2f}',


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
            month_name_heb = fake.month_name_he(month)
            year = salary_date.strftime('%Y')
            common_draw.save_render_html(
                output_path=self.item_context.png_output_path.replace('.png', f'-m{salary_date_num+1}.png'),
                pdf_output_path=self.item_context.pdf_output_path.replace('.pdf', f'-m{salary_date_num+1}.pdf') if self.item_context.pdf_output_path else None,
                render_path='salaries/center.html',
                page=self.html_page,
                http_server_port=self.subtype_context.http_server_port,
                width=2480, height=3600,
                context={
                    **fixed_context,
                    'top_salary_month': f'{month_name_heb} {year}',
                    'mekadmim_shaot_mekadem_misra_klali': f'{fake.random_int(1, 100000) / 100000:,.5f}',
                    'mekadmim_shaot_mekadem_misra_ofek': f'{fake.random_int(1, 100000) / 100000:,.5f}',
                    'mekadmim_shaot_mekadem_havraa': f'{fake.random_int(1, 100000) / 100000:,.5f}',
                    'mekadmim_shaot_shot_avoda': fake.random_int(1, 220),
                    'mekadmim_shaot_shot_avoda_bafoal': fake.random_int(1, 220),
                    'mekadmim_shaot_hashlama_mora_em': fake.random_int(0, 20),
                    'tashlumim_table': {
                        'div_trs_td_div': get_tashlumim_table(fake)
                    },
                    'sahah_tashlumim_hefreshim': f'{fake.random_int(-100000, 100000, step=25)/100:,.2f}',
                    'sahah_tashlumim_hodshi': f'{fake.random_int(-100, 3000000)/100:,.2f}',
                    'nikuey_hova_mas_hachnasa': f'{fake.random_int(100, 100000)/100*fake.random_element([1, -1]):,.2f}' if fake.random_int(1, 2) == 1 else '',
                    'nikuey_hova_bituah_leumi': f'{fake.random_int(100, 100000)/100*fake.random_element([1, -1]):,.2f}' if fake.random_int(1, 2) == 1 else '',
                    'nikuey_hova_bituach_briut': f'{fake.random_int(100, 100000)/100*fake.random_element([1, -1]):,.2f}' if fake.random_int(1, 2) == 1 else '',
                    'nikuey_hova_hefreshey_bituach_leumi': f'{fake.random_int(100, 100000)/100*fake.random_element([1, -1]):,.2f}' if fake.random_int(1, 2) == 1 else '',
                    'nikuey_hova_hefreshey_briut': f'{fake.random_int(100, 100000)/100*fake.random_element([1, -1]):,.2f}' if fake.random_int(1, 2) == 1 else '',
                    'sahah_nikuy_hova': f'{fake.random_int(100, 900000)/100*fake.random_element([1, -1]):,.2f}',
                    'nikuey_gemel_table': {
                        'div_trs_td_div': get_nikuey_gemel_table(fake)
                    },
                    'sahah_nikuy_gemel': f'{fake.random_int(100, 3000000)/100:,.2f}',
                    'nikuyim_aherim_table': {
                        'div_trs_td_div': get_nikuyim_aherim_table(fake)
                    },
                    'sahah_nikyim_aherim': f'{fake.random_int(100, 3000000)/100:,.2f}' if fake.random_int(1, 2) == 1 else '',
                    'neto_shlili': f'{fake.random_int(100, 3000000)/100:,.2f}' if fake.random_int(1, 2) == 1 else '',
                    'sahah_nikuim_aherim_bottom': f'{fake.random_int(100, 3000000)/100:,.2f}' if fake.random_int(1, 2) == 1 else '',
                    'sahah_nikuy_gemel_bottom': f'{fake.random_int(100, 3000000)/100:,.2f}' if fake.random_int(1, 2) == 1 else '',
                    'sahah_nikuy_hova_bottom': f'{fake.random_int(100, 3000000)/100:,.2f}' if fake.random_int(1, 2) == 1 else '',
                    'sahah_tashlumim_bottom': f'{fake.random_int(100, 3000000)/100:,.2f}' if fake.random_int(1, 2) == 1 else '',
                    'shum_babank': f'{fake.random_int(100, 3000000)/100:,.2f}' if fake.random_int(1, 2) == 1 else '',
                },
            )
