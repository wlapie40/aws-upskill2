from common.aws.gateways.boto import _client
# from common.logger import *


def read_parameters_store(param_name: str, with_decryption: bool = False):
    client = _client('ssm')
    # logger.info(f'read_parameters_store: param_name={param_name}, with_decryption={with_decryption}')
    if not param_name:
        raise ValueError("param_name value error. You need to provide parameter store name")
    try:
        return str(client.get_parameter(Name=param_name,
                                    WithDecryption=with_decryption)['Parameter']['Value'])
    except Exception as e:
        print(f'error {str(e)}')
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
