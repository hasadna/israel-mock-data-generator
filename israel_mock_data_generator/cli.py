import click

from . import pdf_multi_config_constants


@click.group()
def main():
    pass


@main.command()
@click.argument('CONFIG_TYPE', type=click.Choice(pdf_multi_config_constants.TYPES.keys()))
@click.argument('NUM', type=int, default=1)
def generate_pdf_multi_config(**kwargs):
    from .generate_pdf_multi_config import main
    main(**kwargs)


if __name__ == '__main__':
    main()
