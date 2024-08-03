def convert_parameters_to_file_format(parameters: dict) -> dict:
    file_format = []
    for parameter in parameters:
        file_format.append({
            'Name': parameter['Name'],
            'Type': parameter['Type'],
            'Value': parameter['Value']
        })
    return file_format
