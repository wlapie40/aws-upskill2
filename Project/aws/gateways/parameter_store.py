import logging as logger
from . boto import _client


def _read_parameters_store(param_store_name: str, with_decryption: bool = False):
    logger.info(f'call _read_parameters_store(param_name={param_store_name})')
    client = _client('ssm')
    try:
        return tuple(client.get_parameter(Name=param_store_name,
                                          WithDecryption=with_decryption)['Parameter']['Value'].split(','))
    except Exception as e:
        print(f'CHECK AWS CREDENTIALS !\nError msg: {e}')
        return False


def _put_parameter_to_store(value: str,
                            name: str = 'sfigiel-sequenceToken',
                            description: str = "the very next 'sequenceToken' for CloudWatch (logs)",
                            value_type: str = 'String',
                            ):
    client = _client('ssm')
    response = client.put_parameter(
        Name=name,
        Description=description,
        Value=value,
        Type=value_type,
        # KeyId='string', # is required for SecureString type parameter only.
        Overwrite=True,
        Tier='Standard',
    )
    logger.info(f'call _put_parameter_to_store() {response}')
