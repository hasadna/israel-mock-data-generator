from .salary import Salary

from .. import common_draw


MAHLAKOT = [m.strip() for m in '''
גזברות, גביה, חשבות, תלונות הציבור, תעבורה, הנדסה, חינוך, חינוך לגיל הרך, תרבות, לוגיסטיקה, לשכה, דיגיטציה של השירות, ביטחון, סייבר, הוראה, פיתוח, תשתיות דיגיטל, תשתיות ענן, שירות לקוחות, שירות שותפים, תחבורה, פיתוח עסקי, עיצוב גרפי.
'''.split(',') if m.strip()]


class SalaryNorth(Salary):

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
        }
        render_html_kwargs = dict(
            template_name='salaries/north',
            page=self.html_page,
            http_server_port=self.subtype_context.http_server_port,
            width=2500, height=3508,
            context=html_context,
        )
        common_draw.save_render_html(
            path=self.item_context.png_output_path.replace('.png', '-p1.png'),
            **render_html_kwargs,
        )
        common_draw.save_render_html(
            path=self.item_context.png_output_path.replace('.png', '-p2.png'),
            y=3508, **render_html_kwargs
        )
