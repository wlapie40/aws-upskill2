from Project.aws.entities.filters import datetimeformat
import json


def serializer(obj : 'dict', filter : 'str' = None) ->'json data':
    if filter:
        json_data = {en + 1: el for en, el in enumerate(obj[filter]) if not None}
    else:
        json_data = {en + 1: el for en, el in enumerate(obj) if not None}
    json_data = json.dumps(json_data, default=datetimeformat)
    json_data = json.loads(json_data)
    return json_data