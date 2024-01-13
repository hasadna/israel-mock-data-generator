import click

from . import pdf_multi_config_constants


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
@click.argument('BANK')
@click.argument('NUM', type=int, default=1)
@click.option('--test', is_flag=True)
@click.option('--no-bg', is_flag=True)
@click.option('--mock', is_flag=True)
@click.option('--no-pdf', is_flag=True)
@click.option('--source-image')
def generate_bank_statements(**kwargs):
    from .generate_bank_statements import main
    main(**kwargs)


@main.command()
@click.argument('PDF_PATH')
def extract_font_names(pdf_path):
    from .extract_font_names import main
    main(pdf_path)


if __name__ == '__main__':
    main()
