from typing import Any

import orjson


# 字符串


def obj_to_json(data: Any) -> str:
    payload = orjson.dumps(data)  # bytes
    return payload.decode('utf-8')  # string


def json_to_obj(json_str: str) -> Any:
    return orjson.loads(json_str)


# 字节


def obj_to_jsonb(data: Any) -> bytes:
    return orjson.dumps(data)


def jsonb_to_obj(json_bytes: bytes) -> Any:
    return orjson.loads(json_bytes)


# 文件


def write_json_file(path: str, data: Any) -> None:
    option = orjson.OPT_INDENT_2
    with open(path, 'wb') as f:
        f.write(orjson.dumps(data, option=option))


def read_json_file(path: str) -> Any:
    with open(path, 'rb') as f:
        return orjson.loads(f.read())
