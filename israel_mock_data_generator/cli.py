import os
import click

from . import pdf_multi_config_constants
from faker_israel.common_draw import start_python_http_server, PRIVATE_DATA_PATH


@click.group()
def main():
    pass


@main.command()
@click.argument('CONFIG_TYPE', type=click.Choice(pdf_multi_config_constants.TYPES.keys()))
@click.argument('NUM', type=int, default=1)
@click.option('--key-prefix')
@click.option('--doc-name')
def generate_pdf_multi_config(**kwargs):
    from .generate_pdf_multi_config import main
    main(**kwargs)


@main.command()
@click.argument('TYPE')
@click.argument('SUBTYPE')
@click.argument('NUM', type=int, default=1)
@click.option('--test', is_flag=True)
@click.option('--no-bg', is_flag=True)
@click.option('--mock', is_flag=True)
@click.option('--no-pdf', is_flag=True)
@click.option('--source-image')
def generate(**kwargs):
    from .generate import main
    kwargs['type_'] = kwargs.pop('type')
    main(**kwargs)


@main.command()
@click.argument('PDF_PATH')
def extract_font_names(pdf_path):
    from .extract_font_names import main
    main(pdf_path)


@main.command()
def start_http_server():
    with start_python_http_server(os.path.join(PRIVATE_DATA_PATH, '..')) as get_port:
        port = get_port()
        print(f'Started HTTP server on port {port}')
        print(f'http://localhost:{port}/israel-mock-data-generator/faker_israel/')
        input('Press Enter to stop server...')


if __name__ == '__main__':
    main()
