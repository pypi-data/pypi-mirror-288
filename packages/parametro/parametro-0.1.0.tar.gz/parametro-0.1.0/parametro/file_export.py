import json

import boto3
import click

from .file_utils import convert_parameters_to_file_format


@click.command()
@click.option('--prefix', help='prefix to export', required=True)
@click.option('--file', help='file to write export into', required=True)
def export_by_prefix(prefix,
                     file):
    """Exports all parameter values under a given prefix."""
    click.echo(f'Starting export for prefix {prefix}')

    client = boto3.client('ssm')

    response = client.get_parameters_by_path(
        Path=prefix,
        Recursive=True,
        WithDecryption=True
    )

    with open(file, 'w', encoding='utf-8') as target_file:
        json.dump(convert_parameters_to_file_format(response['Parameters']), target_file, indent=2)

    click.echo(f'Export has been written to {file}.')
