import datetime

from parametro.file_utils import convert_parameters_to_file_format

EXPECTED_FILE_FORMAT = [
    {
        'Name': '/prefix/MyParam1',
        'Value': '12345test',
        'Type': 'String',
    }
]


def test_convert_parameters_to_file_format():
    response_parameters = [
        {
            'Name': '/prefix/MyParam1',
            'Value': '12345test',
            'Type': 'String',
            'Version': 2,
            'LastModifiedDate': datetime.datetime(2024, 7, 31, 12, 36, 12, 28000)
        }
    ]
    assert convert_parameters_to_file_format(response_parameters) == EXPECTED_FILE_FORMAT
