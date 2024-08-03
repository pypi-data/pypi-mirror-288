import json

import boto3
import click


@click.command()
@click.option('--file', help='file to load parameters from export into', required=True)
def import_from_file(file):
    """Imports all parameter values from a given file."""
    with open(file, encoding='utf-8') as target_file:
        parameters = json.load(target_file)

    client = boto3.client('ssm')
    for parameter in parameters:
        click.echo(f"Updating parameter {parameter['Name']}")
        client.put_parameter(
            Name=parameter['Name'],
            Type=parameter['Type'],
            Value=parameter['Value'],
            Overwrite=True
        )

    click.echo('Done.')
