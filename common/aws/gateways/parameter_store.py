from common.aws.gateways.boto import _client


def read_parameters_store(param_name: str, region_name: str, with_decryption: bool = False):
    client = _client(service='ssm', region_name=region_name)
    if not param_name:
        raise ValueError("param_name value error. You need to provide parameter store name")
    try:
        return str(client.get_parameter(Name=param_name,
                                        WithDecryption=with_decryption)['Parameter']['Value'])
    except Exception as e:
        print(f'error {str(e)}')
        return None
