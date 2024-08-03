import click

from .file_export import export_by_prefix
from .file_import import import_from_file


@click.group()
def cli():
    pass


cli.add_command(export_by_prefix)
cli.add_command(import_from_file)


def main():
    cli()


if __name__ == '__main__':
    main()
