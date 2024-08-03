import tempfile

from click.testing import CliRunner
from moto import mock_aws

from parametro.file_export import export_by_prefix
from tests.testdata import DEMO_EXPORT, DEMO_PREFIX, setup_demo_prefix


@mock_aws
def test_export_by_prefix():
    setup_demo_prefix()

    target_file = tempfile.NamedTemporaryFile()

    runner = CliRunner()
    result = runner.invoke(export_by_prefix, ['--prefix', DEMO_PREFIX, '--file', target_file.name])
    assert result.exit_code == 0

    with open(target_file.name) as target_fp:
        file_contents = target_fp.read()

    assert file_contents == DEMO_EXPORT
