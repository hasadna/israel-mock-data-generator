import os
from contextlib import contextmanager

from ..common_draw import init_html_page, start_python_http_server, PRIVATE_DATA_PATH


class SalaryRootContext:

    def __init__(self, fake, **kwargs):
        self.fake = fake


class SalarySubtypeContext:

    def __init__(self, root_context, subtype, subtype_class, test=False, html_page=None, http_server_get_port=None, **kwargs):
        self.root_context = root_context
        self.subtype = subtype
        self.subtype_class = subtype_class
        self.test = test
        self.html_page = html_page
        self.http_server_get_port = http_server_get_port
        self._http_server_port = None

    @property
    def http_server_port(self):
        if self._http_server_port is None:
            self._http_server_port = self.http_server_get_port()
        return self._http_server_port


class SalaryItemContext:

    def __init__(self, subtype_context, i=None, png_output_path=None, pdf_output_path=None, **kwargs):
        self.root_context = subtype_context.root_context
        self.subtype_context = subtype_context
        if self.subtype_context.test:
            self.i = 0
            self.png_output_path = 'test.png'
            self.pdf_output_path = None
        else:
            self.i = i
            self.png_output_path = png_output_path
            self.pdf_output_path = pdf_output_path
        self.salary = self.subtype_context.subtype_class(self)
        print(f'Initialized SalaryItemContext {i}')

    def generate(self):
        self.salary.generate()


@contextmanager
def salaries_generate_context(**kwargs):
    yield SalaryRootContext(**kwargs)


@contextmanager
def salary_generate_context(root_context, **kwargs):
    with start_python_http_server() as get_port:
        with init_html_page() as html_page:
            yield SalarySubtypeContext(
                root_context,
                html_page=html_page,
                http_server_get_port=get_port,
                **kwargs
            )


@contextmanager
def salary_item_generate_context(subtype_context, **kwargs):
    yield SalaryItemContext(subtype_context, **kwargs)


class Salary:

    def __init__(self, subtype_id, item_context):
        self.subtype_id = subtype_id
        self.item_context = item_context
        self.subtype_context = self.item_context.subtype_context
        self.root_context = self.subtype_context.root_context
        self.fake = self.root_context.fake
        self.html_page = self.subtype_context.html_page
