import json


def dict_to_json(data):
    return json.dumps(data, ensure_ascii=False)


def json_to_dict(json_data):
    return json.loads(json_data)
