import boto3

DEMO_PREFIX = '/demo'

DEMO_EXPORT = '''[
  {
    "Name": "/demo/param1",
    "Type": "String",
    "Value": "test1234"
  },
  {
    "Name": "/demo/param2",
    "Type": "String",
    "Value": "test56789"
  }
]'''


def setup_demo_prefix():
    client = boto3.client('ssm')
    client.put_parameter(Name='/demo/param1', Value='test1234', Type='String')
    client.put_parameter(Name='/demo/param2', Value='test56789', Type='String')


def assert_demo_parameters(parameters):
    assert len(parameters) == 2

    assert parameters[0]['Name'] == '/demo/param1'
    assert parameters[0]['Type'] == 'String'
    assert parameters[0]['Value'] == 'test1234'

    assert parameters[1]['Name'] == '/demo/param2'
    assert parameters[1]['Type'] == 'String'
    assert parameters[1]['Value'] == 'test56789'
