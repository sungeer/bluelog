import json
from datetime import datetime, date
from decimal import Decimal


def dict_to_json(data):
    return json.dumps(data, cls=JsonExtendEncoder, ensure_ascii=False)


def dict_to_json_stream(data):
    return json.dumps(data, cls=JsonExtendEncoder, ensure_ascii=False).encode('utf-8')


def json_to_dict(json_data):
    return json.loads(json_data)


class JsonExtendEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, (tuple, list, datetime)):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        elif isinstance(obj, Decimal):
            return float(obj)
        elif isinstance(obj, bytes):
            return obj.decode('utf-8')
        return super().default(obj)
