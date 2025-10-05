import orjson


def dict_to_json(data):
    return orjson.dumps(data).decode('utf-8')


def json_to_dict(json_data):
    return orjson.loads(json_data)
