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


def get_another_block(fake, block_name):
    # 1-3 lines
    number_of_lines = fake.random_int(1, 3)

    DESCS = [
            'שעות נוספות 125%',
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
            'ביגוד'
    ]
    if (block_name == 'שכר עבודה'):
        DESCS.append('שכר בסיס')
        DESCS.append('שכר חודשי')

    descs = set(DESCS)

    res = []

    # block header - Todo - should it be part of the returned array??
    block_header = block_name
    res.append(block_header)    # ???

    for i in range(1, number_of_lines):
        desc = fake.random_element(list(descs))
        descs.remove(desc)

        res.append([
            fake.numerify("####"),  # סמל
            desc,
            fake.random_element(['', fake.random_int(1, 1000), fake.random_element(['קבוע', 'זמני'])]), # למידע
            fake.random_element(['', random_float(fake, 1, 300)]),  # תעריף
            fake.random_element(['', random_float(fake, 1, 200)]),  # אחוז
            fake.random_element(['', fake.random_int(-100, 100)]),  # כמות
            fake.random_element(['', random_float(fake, -9999, 9999)]),    # סכום לתשלום
        ])
        
    # ToDo - line of sach-hakol should be part of array?
    res.append([
        fake.random_element(['', fake.random_int(1, 1000)]),    # סה"כ
    ])
    
    return res


def get_nikuyim_vehafrashot_table(fake):
    # number of lines: 1-7
    number_of_lines = fake.random_int(1, 7)

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
    gemel = set(GEMEL)

    res = []
    for i in range(1, number_of_lines):
        kupat_gemel_desc = fake.random_element(list(gemel))
        gemel.remove(kupat_gemel_desc)

        res.append([
            fake.numerify("###"),
            kupat_gemel_desc,
            fake.random_element(['קצבה שכיר','פיצויים']),
            '',
            fake.random_element(['', random_float(fake, -999, 9999)]),
            fake.random_element(['', random_float(fake, -999, 9999)]),
            fake.random_element(['', random_float(fake, -999, 9999)])
                    ]) 
 
    # sach kupot gemel beheskem - not sure if it is in the table or outside!! - currently outside
    return res


def get_taarifim_table(fake):
    descs = set([
        'יום',
        'שעה',
        'משכורת',
    ])
    res = []

    desc = fake.random_element(list(descs))
    descs.remove(desc)
    res.append([desc, random_float(fake, 1, 2000)])

    desc = fake.random_element(list(descs))
    descs.remove(desc)
    res.append([desc, random_float(fake, 1, 2000)])

    return res


def get_nikuyei_chova_misim_table(fake):
    res = []
    res.append([
                fake.random_element(['', random_float(fake, -99999, 99999)]),
                fake.random_element(['', random_float(fake, -99999, 99999)]),
                fake.random_element(['', random_float(fake, -99999, 99999)]),
                fake.random_element(['', random_float(fake, -99999, 99999)]),
                fake.random_element(['', random_float(fake, -99999, 99999)]),
                ])
    return res


def get_nikuyei_hitchayvut_table(fake):
    descs = set([
        'קו הבריאות',
        'תשלומים לעירייה',
        'ביטוח שיניים',
        'החזרי הלוואות',
        'השתתפות בקורס',
    ])

    res = []
    # 1-2 lines. So first line always exists, second line sometimes
    desc = fake.random_element(list(descs))
    descs.remove(desc)
    res.append([fake.numerify("###"),
                desc,
                fake.random_element(['', random_float(fake, 0.5, 100)]),    # ToDo not sure 0.5 is legal arg here
                fake.random_element(['', fake_date(fake)]),
                fake.random_element(['', fake.random_int(1, 100)]),
                fake.random_element(['', fake.random_int(1, 1000)]),
                fake.random_element(['', fake.random_int(1, 1000)]),
                fake.random_element(['', fake.random_int(1, 9999)]),
                random_float(fake, 1, 9999)
                ])
    # 2nd row only in 50% of salaries
    if (fake.random_element(['y','n']) == 'y'):
        desc = fake.random_element(list(descs))
        descs.remove(desc)  # actually not necessary here
        res.append([desc, 
                random_float(fake, 1, 999999), random_float(fake, 0, 99999), random_float(fake, 0, 99999), 
                f'{fake.random_int(0, 1250, step=25) / 100:,.2f}'  # 0-12.5 step 0.25
                ])
    # possibly we need in the else to append an empty line?
    # else:
    #     res.append(['', '', ''])

    return res


def get_netunim_miztabrim_kupot_gemel_table(fake):
    res = []
    res.append(['קרן השתלמות', 
                random_float(fake, 1, 999999), random_float(fake, 0, 99999), random_float(fake, 0, 99999), 
                f'{fake.random_int(0, 1250, step=25) / 100:,.2f}'  # 0-12.5 step 0.25
                ])
    res.append(['תגמולים לקצבה', 
                random_float(fake, 1, 999999), random_float(fake, 0, 99999), random_float(fake, 0, 99999), 
                f'{fake.random_int(0, 1250, step=25) / 100:,.2f}'  # 0-12.5 step 0.25
                ])
    return res


def get_heiadruyot_table(fake):
    res = []
    res.append(['חופשה בשעות', random_float(fake, 1, 240), random_float(fake, 0, 999), random_float(fake, 1, 30), 
                               fake.random_element(['', random_float(fake, 1, 240)]), 
                               random_float(fake, 1, 240), random_float(fake, 1, 999), random_float(fake, 1, 999) 
                ])
    res.append(['הבראה', random_float(fake, 1, 20), '', random_float(fake, 0, 1), 
                               random_float(fake, 0, 1), 
                               random_float(fake, 1, 240), random_float(fake, 1, 999), '' 
                ])
    res.append(['מחלה בשעות', random_float(fake, 1, 240), random_float(fake, 0, 999), random_float(fake, 1, 30), 
                               fake.random_element(['', random_float(fake, 1, 240)]), 
                               random_float(fake, 1, 240), random_float(fake, 1, 999), random_float(fake, 1, 999) 
                ])
    return res


def random_float(fake, start, end):
    return f'{fake.random_int(100*start, 100*end)/100:,.2f}'


def fake_date(fake):
    return fake.date_between(start_date='-3y', end_date='-1y').strftime('%d/%m/%y')


def get_perut_tashlumim_table_html(fake):
    shar_avoda_block_title = 'שכר עבודה'
    block_titles = {
        shar_avoda_block_title,
        'תשלומים בגין שעות נוספות ומאמץ מיוחד',
        'תשלומים בגין הוצאות',
        'תשלומים אחרים',
        'החזר הוצאות נטו',
    }
    teurs = {
        'שעות נוספות 125%',
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
    }
    html = '<table><tbody>'
    html += '''<tr style="height: 9px;">
        <td style="width: 85px;"></td>
        <td style="width: 299px;"></td>
        <td style="width: 263px;"></td>
        <td style="width: 228px;"></td>
        <td style="width: 201px;"></td>
        <td style="width: 144px;"></td>
        <td style="width: 198px;"></td>
        <td style="width: 100%;"></td>
    </tr>'''
    num_blocks = fake.random_int(1, 4)
    block_num_rows = [fake.random_int(1, 3) for _ in range(num_blocks)]
    if num_blocks == 4:
        while sum(block_num_rows) > 9:
            block_num_rows[fake.random_int(0, 3)] -= 1
    for i in range(num_blocks):
        block_title = fake.random_element(list(block_titles))
        block_titles.remove(block_title)
        html += f'''<tr class="pt">
            <td colspan="8"><div>{block_title}</div></td>
        </tr>'''
        num_rows = block_num_rows[i]
        for _ in range(num_rows):
            semel = f'{fake.random_int(1, 9999):03d}'
            if block_title == shar_avoda_block_title:
                teur = fake.random_element(['שכר בסיס', 'שכר חודשי'])
            else:
                teur = fake.random_element(list(teurs))
                teurs.remove(teur)
            lemeida_type = fake.random_element(['empty', 'number', 'text'])
            if lemeida_type == 'empty':
                lemeida = ''
            elif lemeida_type == 'number':
                lemeida = fake.random_int(1, 1000)
            else:
                lemeida = fake.random_element(['קבוע', 'זמני'])
            taarif = random_float(fake, 1, 300) if fake.random_int(1, 2) == 1 else ''
            ahuz = random_float(fake, 1, 200) if fake.random_int(1, 2) == 1 else ''
            kamut = random_float(fake, 1, 200) if fake.random_int(1, 2) == 1 else ''
            if kamut and fake.random_int(1, 4) == 1:
                kamut = '-' + kamut
            shum = random_float(fake, 1, 9999) if fake.random_int(1, 2) == 1 else ''
            if shum and fake.random_int(1, 4) == 1:
                shum = '-' + shum
            html += f'''<tr class="pr">
                <td><div>{semel}</div></td>
                <td colspan="2"><div>{teur}</div></td>
                <td><div>{lemeida}</div></td>
                <td><div>{taarif}</div></td>
                <td><div>{ahuz}</div></td>
                <td><div>{kamut}</div></td>
                <td><div>{shum}</div></td>
            </tr>'''
        sahah = random_float(fake, 1, 9999)
        html += f'''<tr class="ps">
            <td colspan="2"><div></div></td>
            <td colspan="5"><div>סה"כ {block_title}</div></td>
            <td><div>{sahah}</div></td>
        </tr>'''
    return html


def get_zkifot_sahar_items(fake):
    descriptions = {
        'שווי רכב',
        'שווי ארוחות',
        'קה"ש מעל התקרה',
        'שווי מתנה נטו',
        'שווי שי לחג',
        'שווי בונוס נטו',
    }
    res = {}
    num_rows = fake.random_int(1, 3)
    for i in range(3):
        istr = {
            0: 'first',
            1: 'second',
            2: 'third'
        }
        if i < num_rows:
            res[f'semel_{istr[i]}'] = f'{fake.random_int(1, 9999):03d}'
            description = fake.random_element(list(descriptions))
            descriptions.remove(description)
            res[f'description_{istr[i]}'] = description
            res[f'untitled_{istr[i]}'] = fake.random_element(['', 'קבוע', 'גילום'])
            res[f'kamut_{istr[i]}'] = fake.random_element(['', '1.0'])
            res[f'sum_tkina_{istr[i]}'] = random_float(fake, 1, 999)
            res[f'sum_gilum_{istr[i]}'] = random_float(fake, 1, 999) if fake.random_int(1, 2) == 1 else ''
        else:
            res[f'semel_{istr[i]}'] = ''
            res[f'description_{istr[i]}'] = ''
            res[f'untitled_{istr[i]}'] = ''
            res[f'kamut_{istr[i]}'] = ''
            res[f'sum_tkina_{istr[i]}'] = ''
            res[f'sum_gilum_{istr[i]}'] = ''
    return res


class SalaryEast(Salary):

    def generate(self):
        fake = self.fake
        machlaka_number = fake.random_int(50, 99999)
        tz_number = fake.teudat_zehut()
        fixed_context_page_1 = {
            'company': fake.company(),
            'address_company': f', {fake.street_address()}, {fake.city()}, {fake.postcode()}',
            'tik_nikuyim': fake.numerify("#########"),
            'company_number': 'חברה : ' + fake.numerify("#########"),
            'department': f'{machlaka_number} פיתוח ממשלה',
            'full_name': fake.first_name() + ' ' + fake.last_name(),
            'address_person': fake.street_address(),
            'city_zip': f'{fake.city()}, {fake.postcode()}',
        }
        first_year = fake.random_int(2012, 2022)
        first_month = fake.random_int(1, 10)
        first_date = datetime.date(first_year, first_month, 1)
        for salary_date_num, salary_date in enumerate([
            first_date,
            # first_date + relativedelta(months=1),
            # first_date + relativedelta(months=2),
        ]):
            month_name_he = fake.month_name_he(salary_date.month)
            common_draw.save_render_html(
                output_path=self.item_context.png_output_path.replace('.png', f'-m{salary_date_num+1}.png'),
                pdf_output_path=self.item_context.pdf_output_path.replace('.pdf', f'-m{salary_date_num+1}.pdf') if self.item_context.pdf_output_path else None,
                render_path='salaries/east-page-1.html',
                page=self.html_page,
                http_server_port=self.subtype_context.http_server_port,
                width=2480, height=3507,
                context={
                    **fixed_context_page_1,
                    'tlush_date': f'{month_name_he} {salary_date.year}',
                    'perut_tashlumim_table': get_perut_tashlumim_table_html(fake),
                    'semel_work_hours': f'{fake.random_int(1, 9999):03d}',
                    'work_hours_float': fake.random_int(1, 300),
                    'semel_hours_employer_allowance': f'{fake.random_int(1, 9999):03d}',
                    'hours_employer_allowance_float': fake.random_int(1, 300),
                    **get_zkifot_sahar_items(fake),
                    'total_sum_zkifut': random_float(fake, 1, 9999),
                    'total_sum_tashlumim': random_float(fake, 1, 9999),
                }
            )
