import datetime

from .salary import Salary

from .. import common_draw


MAHLAKOT = [m.strip() for m in '''
גזברות, גביה, חשבות, תלונות הציבור, תעבורה, הנדסה, חינוך, חינוך לגיל הרך, תרבות, לוגיסטיקה, לשכה, דיגיטציה של השירות, ביטחון, סייבר, הוראה, פיתוח, תשתיות דיגיטל, תשתיות ענן, שירות לקוחות, שירות שותפים, תחבורה, פיתוח עסקי, עיצוב גרפי.
'''.split(',') if m.strip()]

HEHZER_HOZAOT_TYPES = [item.strip() for item in '''
    הוצאות קבועות-נטו
    החזר הוצאות קבועות
    ביטוח רכב חובה
    ביטוח רכב מקיף
    אגרת רישוי
    אגרת רישוי-נטו
    נסיעות
    נסיעות קבועות
    ביגוד שנתי רמה1
    ביגוד שנתי רמה2
    ביגוד שנתי רמה3
    ביגוד שנתי רמה4
    ביגוד שנתי רמה5
    ביגוד שנתי רמה6
    ביגוד שנתי רמה7
    ביגוד שנתי רמה8
    ביגוד שנתי רמה9
    מענק שנתי
    מענק חודשי
    מענק חד פעמי
    מענק רבעוני
    שכר עידוד
    בונוס שנתי
    בונוס חודשי
    בונוס חד פעמי
    בונוס רבעוני
    טלפון
    תשלום שיחות טלפון
    תן ביס
    קורס/לימודים
    השתלמות
    נפש
    מקדמות שכר
    החזר נסיעות חול
    החזר נסיעות דלק/מונית
    הוצאות אחרות
    ביגוד
    דמי חבר אירגון מקצועי
'''.split('\n') if item.strip()]


class SalaryNorth(Salary):

    def get_main_table_rows_rows(self, mahlaka_code, type_, min_rows, max_rows):
        fake = self.fake
        rows = []
        num_rows = fake.random_int(min_rows, max_rows)
        for _ in range(num_rows):
            kamut = fake.random_element(['', '1'])
            ahuz = fake.random_element(['', '', 10000, 10000, 10000, 99999])
            taarif = fake.random_element(['', '', 42000])
            yitra = fake.random_element(['', '', 999999])
            if yitra:
                yitra = (10000, yitra)
            lemeida = fake.random_element(['', '', 'קבוע', 'זמני'])
            shum = fake.random_element(['', '', 300000])
            if shum:
                shum = (15000, shum)
            if type_ == 'tosafot_pensioniot':
                desc = fake.random_element(
                    ['תוספת באחוזים', 'תוספת ע"פ חוק', 'הסכם שכר', 'תוספת', 'תוספת שקלית', 'תוספת אחוזית'])
                if desc == 'הסכם שכר':
                    desc += ' - ' + fake.date_between(start_date=datetime.date(1999, 1, 1), end_date=datetime.date(2022, 1, 1)).strftime('%Y')
                elif desc in ['תוספת', 'תוספת שקלית', 'תוספת אחוזית']:
                    desc += ' - ' + fake.date_between(start_date=datetime.date(2000, 1, 1), end_date=datetime.date(2022, 1, 1)).strftime('%Y')
            elif type_ == 'hehzer_hozaot':
                desc = fake.random_element(HEHZER_HOZAOT_TYPES)
                shum = (15000, 300000)
            elif type_ == 'tashlumim_nosafim':
                desc = fake.random_element(['מקדמה', 'גילום', 'גילום תשלום שנתי', 'גילום תשלום שנתיים', 'החזר חוב'])
                kamut = ''
                ahuz = ''
                taarif = ''
                yitra = ''
                lemeida = ''
                shum = (-500000, 1500000)
            elif type_ == 'rehivey_avoda_nosefet':
                desc = fake.random_element(['שעות נוספות', 'ש.נ.', 'ש.נ. נוכחות'])
                shum = (15000, 300000)
            elif type_ == 'shovi_lemas':
                desc = fake.random_element(['מתנות לחישוב מס', 'הפרשים חייבים במס', 'הפרשה חייבת במס'])
                kamut = ''
                ahuz = ''
                taarif = ''
                yitra = (-1000000, 1000000)
                lemeida = ''
                shum = ''
            else:
                raise Exception(f'Unknown type: {type_}')
            if kamut:
                kamut = fake.random_int(5, 100) / 10
            if ahuz:
                ahuz = fake.random_int(1, ahuz) / 100
            if taarif:
                taarif = fake.random_int(2800, taarif) / 100
            if yitra:
                yitra = fake.random_int(*yitra) / 100
            if shum:
                shum = fake.random_int(*shum) / 100
            rows.append([
                str(fake.random_int(1, 999)),
                desc,
                mahlaka_code,
                f'{kamut:,.2f}' if kamut else '',
                f'{ahuz:,.2f}' if ahuz else '',
                f'{taarif:,.2f}' if taarif else '',
                f'{yitra:,.2f}' if yitra else '',
                lemeida,
                f'{shum:,.2f}' if shum else '',
            ])
        for _ in range(max_rows-num_rows):
            rows.append(['', '', '', '', '', '', '', '', ''])
        return rows

    def generate(self):
        fake = self.fake
        company = fake.company()
        street_address = fake.street_address()
        city = fake.city()
        rashut = fake.random_element(["58", "42"])
        tik_nikuim = fake.numerify("#########")
        tik_bl = f'{tik_nikuim}00'
        mahlaka_code = fake.numerify('#######').lstrip('0')
        mahlaka_name = fake.random_element(MAHLAKOT)
        mahlaka = mahlaka_code + ' ' + mahlaka_name
        month = fake.date('%m')
        month_name_heb = fake.month_name_he(month)
        year = fake.date_between(start_date='-10y').strftime('%Y')
        siduri = fake.numerify('####')
        rcpt_first_name = fake.first_name()
        rcpt_last_name = fake.last_name()
        rcpt_street = fake.street_address()
        rcpt_city = fake.city()
        rcpt_zip = fake.postcode()
        data_misra_tashlumim = fake.random_int(1000, 50000) + fake.random_int(0, 99) / 100
        data_nikuim_ishiim_hova = fake.random_int(25, 40) * data_misra_tashlumim / 100
        data_neto_payment = data_misra_tashlumim - data_nikuim_ishiim_hova
        mispar_zehut = fake.teudat_zehut()
        date_of_birth = fake.date_between(start_date='-60y', end_date='-25y')
        start_of_work_date = fake.date_between(start_date=date_of_birth + datetime.timedelta(days=365*20), end_date='-2y')
        tokef_misra_1 = fake.date_between(start_date=start_of_work_date, end_date='-1y').strftime('%d/%m/%Y')
        bruto_pension = fake.random_int(5000, 15000) + fake.random_int(0, 99) / 100
        mas_hachnasa_type = 'רגיל'
        family_state = fake.random_element(['נשוי/אה', 'רווק/ה', 'גרוש/ה', 'אלמן/ה'])
        partner_income = fake.random_element(['כן', 'לא'])
        bituah_leumi_type = fake.random_element(['רגיל', 'נכות', 'פנסיונר', 'סטודנט', 'גמלאי'])
        workers_association = fake.random_element(['הסתדרות כללית', 'הסתדרות החדשה', ''])
        medical_association = fake.random_element(['כללית', 'מאוחדת', 'מכבי', 'לאומית'])
        misra_type = '1 - יחידה'
        maamad = 'חודשי'
        mas_hachnasa_month_from = fake.random_int(1, 10)
        mas_hachnasa_month_to = fake.random_int(mas_hachnasa_month_from, 12)
        mas_hachnasa_months = []
        for i in range(1, 13):
            if mas_hachnasa_month_from <= i <= mas_hachnasa_month_to:
                mas_hachnasa_months.append('כ')
            else:
                mas_hachnasa_months.append('')
        basis_misra = fake.random_int(10, 100)
        html_context = {
            'topHeader_address': f'{company} , {street_address} {city}',
            'topHeader_rashut': rashut,
            'topHeader_tikNikuim': tik_nikuim,
            'topHeader_hetPey': '',
            'topHeader_tikBL': tik_bl,
            'topHeader_mahlaka': mahlaka,
            'topHeader_month': month_name_heb,
            'topHeader_year': year,
            'topHeader_siduri': siduri,
            'rcpt_lastFirstName': f'{rcpt_last_name} {rcpt_first_name}',
            'rcpt_streetAddress': rcpt_street,
            'rcpt_city': rcpt_city,
            'rcpt_mikud': rcpt_zip,
            'rcpt_returnAddress': f'{company} , {street_address} {city} - יח\' {mahlaka}',
            'rikuz_misraTashlumim': f'{data_misra_tashlumim:,.2f}',
            'rikuz_nikuim_hova': f'{data_nikuim_ishiim_hova:,.2f}',
            'rikuz_netoPayment': f'{data_neto_payment:,.2f}',
            "perutNetuneyMisra_sugHamarkiv": "עבודה",
            "perutNetuneyMisra_mahlaka": mahlaka_code,
            "perutNetuneyMisra_derug": fake.random_element(['עו"ס', 'מ"ח', 'רו"ח', 'עו"ד', 'מח"ר']),
            "perutNetuneyMisra_darga": "מ.א",
            "perutNetuneyMisra_rama": fake.random_element(['א', 'ב', 'ג', 'ד', 'ה', 'ו', 'ז', 'ח', 'ט', 'י']),
            "perutNetuneyMisra_shautBafoal": "",
            "perutNetuneyMisra_basisMisra": str(basis_misra),
            "perutNetuneyMisra_empty": str(basis_misra) + '.0',
            "perutNetuneyMisra_zahal": f'{fake.random_int(0, 2000)/10:,.2f}',
            "perutNetuneyMisra_mukar": f'{fake.random_int(0, 2000)/10:,.2f}',
            "perutNetuneyMisra_avoda": f'{fake.random_int(0, 2000)/10:,.2f}',
            "perutNetuneyMisra_meyuhedet": "",
            "perutNetuneyMisra_yoker": "",
            "perutNetuneyMisra_izun": "",
            "perutNetuneyMisra_ajuzit": f'{fake.random_int(1000, 9999)/10:,.2f}',
            "perutNetuneyMisra_vetek": f'{fake.random_int(100, 9999)/10:,.0f}',
            "perutNetuneyMisra_scharYesod": f'{fake.random_int(100000, 5000000)/100:,.2f}',
            "perutNetuneyMisra_sachar": f'{fake.random_int(100000, 5000000)/100:,.2f}',
            "perutNetuneyMisra_sahach": f'{fake.random_int(100000, 5000000)/100:,.2f}',
            "netunimNosafim": {
                'divs': [
                    mispar_zehut,
                    date_of_birth.strftime('%d/%m/%Y'),
                    start_of_work_date.strftime('%d/%m/%Y'),
                    tokef_misra_1,
                    f'{bruto_pension:,.2f}',
                    mas_hachnasa_type,
                    family_state,
                    partner_income,
                    bituah_leumi_type,
                    workers_association,
                    medical_association,
                    misra_type,
                    maamad,
                ]
            },
            'perutVetakimNosafim': {
                'trs_td_div': [
                    [fake.random_element(['עו"ס', 'מ"ח', 'רו"ח', 'עו"ד', 'מח"ר']), mahlaka_code, fake.random_element(['חדש', 'נמרץ', 'מוכר', 'וותיק']), f'{fake.random_int(50,2000)/100:,.2f}'],
                    [fake.random_element(['עו"ס', 'מ"ח', 'רו"ח', 'עו"ד', 'מח"ר']), mahlaka_code, fake.random_element(['חדש', 'נמרץ', 'מוכר', 'וותיק']), f'{fake.random_int(50,2000)/100:,.2f}'],
                ]
            },
            'pirteyHeshbonBank': {
                'trs_td_div': [
                    [fake.numerify('######'), fake.random_int(10, 999), str(fake.random_int(10, 19)) + ' ' + fake.random_element(['פועלים', 'דיסקונט', 'מזרחי', 'ירושלים', 'יהב'])],
                ]
            },
            'tosafotPensioniot': {
                'trs_td_div': self.get_main_table_rows_rows(mahlaka_code, 'tosafot_pensioniot', 3, 10)
            },
            'tosafotPensioniot_total': f'{bruto_pension:,.2f}',
            'hehzerHozaot': {
                'trs_td_div': self.get_main_table_rows_rows(mahlaka_code, 'hehzer_hozaot', 1, 9)
            },
            'hehzerHozaot_total': f'{fake.random_int(300000,1500000)/100:,.2f}',
            'tashlumimNosafim': {
                'trs_td_div': self.get_main_table_rows_rows(mahlaka_code, 'tashlumim_nosafim', 1, 3)
            },
            'tashlumimNosafim_total': f'{fake.random_int(-500000,1500000)/100:,.2f}',
            'rehiveiAvodaNosefet': {
                'trs_td_div': self.get_main_table_rows_rows(mahlaka_code, 'rehivey_avoda_nosefet', 1, 3)
            },
            'rehiveiAvodaNosefet_total': f'{fake.random_int(300000,1500000)/100:,.2f}',
            'shoviLemas': {
                'trs_td_div': self.get_main_table_rows_rows(mahlaka_code, 'shovi_lemas', 1, 2)
            },
            'shoviLemas_total': f'{fake.random_int(-1000000,1000000)/100:,.2f}',
            'masHachnasa_months': {
                'divs': mas_hachnasa_months
            },
            'masHachnasa': {
                'trs_td_div': [
                    ['', str(mas_hachnasa_month_to-mas_hachnasa_month_from+1), '', str(fake.random_int(100, 300))],
                    ['', str(fake.random_int(0, 500, step=25)/100), '', str(fake.random_int(0, 60))],
                    ['', str(fake.random_int(0, 12)), '', str(fake.random_int(0, 30))],
                ]
            },
            'taarifimIshiimKlalim': {
                'trs_td_div': [
                    ['תעריף יום', str(fake.random_int(1, 999)), f'{fake.random_int(3100, 60000)/100:,.2f}'],
                    ['תעריף שעה', str(fake.random_int(1, 999)), f'{fake.random_int(3100, 60000)/100:,.2f}'],
                    ['שעה מורחב', str(fake.random_int(1, 999)), f'{fake.random_int(3100, 60000)/100:,.2f}'],
                    ['יום מורחב', str(fake.random_int(1, 999)), f'{fake.random_int(3100, 60000)/100:,.2f}'],
                ]
            },
            'shumimMitzbarim': {
                'divs': [
                    f'{fake.random_int(20000, 15000000)/100:,.2f}',
                    f'{fake.random_int(20000, 15000000)/100:,.2f}',
                    f'{fake.random_int(20000, 15000000)/100:,.2f}',
                    f'{fake.random_int(20000, 15000000)/100:,.2f}',
                    f'{fake.random_int(20000, 15000000)/100:,.2f}',
                ]
            }
        }
        common_draw.save_render_html(
            output_path=self.item_context.png_output_path.replace('.png', '-p1.png'),
            render_path='salaries/north_page1.html',
            page=self.html_page,
            http_server_port=self.subtype_context.http_server_port,
            width=2500, height=3508,
            context=html_context,
        )
