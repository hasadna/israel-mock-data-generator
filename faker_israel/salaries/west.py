import datetime
from dateutil.relativedelta import relativedelta

from .salary import Salary

from .. import common_draw, common


class SalaryWest(Salary):

    def generate(self):
        fake = self.fake
        fixed_context = {}
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
                },
            )
