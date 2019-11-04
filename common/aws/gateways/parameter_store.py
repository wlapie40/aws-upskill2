# from common.run import logger
from . boto import _client


def read_parameters_store(param_name: str, with_decryption: bool = False):
    # logger.info(f'call _read_parameters_store(param_name={param_name})')
    client = _client('ssm')
    try:
        return str(client.get_parameter(Name=param_name,
                                    WithDecryption=with_decryption)['Parameter']['Value'])
    except Exception as e:
        # logger.error(f'read_parameters_store ERROR: {e}')
        # logger.error(f'CHECK AWS CREDENTIALS !\nError msg: {e}')
        return None


# def _put_parameter_to_store(value: str,
#                             name: str = 'sfigiel-sequenceToken',
#                             description: str = "the very next 'sequenceToken' for CloudWatch (logs)",
#                             value_type: str = 'String',
#                             ):
#     client = _client('ssm')
#     response = client.put_parameter(
#         Name=name,
#         Description=description,
#         Value=value,
#         Type=value_type,
#         # KeyId='string', # is required for SecureString type parameter only.
#         Overwrite=True,
#         Tier='Standard',
#     )
#     logger.info(f'call _put_parameter_to_store() {response}')
