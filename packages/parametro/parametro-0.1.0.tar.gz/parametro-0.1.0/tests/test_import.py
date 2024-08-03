import tempfile

import boto3
from click.testing import CliRunner
from moto import mock_aws

from parametro.file_import import import_from_file
from tests.testdata import DEMO_EXPORT, DEMO_PREFIX, assert_demo_parameters


@mock_aws
def test_import_from_file():
    target_file = tempfile.NamedTemporaryFile()

    with open(target_file.name, 'w') as target_fp:
        target_fp.write(DEMO_EXPORT)

    runner = CliRunner()
    result = runner.invoke(import_from_file, ['--file', target_file.name])
    assert result.exit_code == 0

    client = boto3.client('ssm')
    response = client.get_parameters_by_path(
        Path=DEMO_PREFIX,
        Recursive=True,
        WithDecryption=True
    )

    assert_demo_parameters(response['Parameters'])
