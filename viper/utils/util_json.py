import orjson


def dict_to_json(data):
    payload = orjson.dumps(data)  # bytes
    return payload.decode('utf-8')  # string


def json_to_dict(json_data):
    return orjson.loads(json_data)
