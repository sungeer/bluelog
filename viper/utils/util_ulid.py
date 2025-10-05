import os
import time

# Crockford Base32 字母表（不含 I L O U，大小写不敏感，这里用大写）
_ALPHABET = '0123456789ABCDEFGHJKMNPQRSTVWXYZ'


def _to_base32(value: int, length: int) -> str:
    chars = []
    for _ in range(length):
        chars.append(_ALPHABET[value & 0b11111])  # 取低5位
        value >>= 5
    chars.reverse()
    return ''.join(chars)


def new_time_sortable_id() -> str:
    """
    生成 26 位大写字符串：10位时间（毫秒） + 16位随机，共 128bit
    字典序 == 时间序；全局唯一概率极高
    """
    # 1) 时间戳（毫秒），48位 -> 10 个 base32 字符（10 * 5 = 50 位）
    ts_ms = int(time.time() * 1000)
    time_part = _to_base32(ts_ms, 10)

    # 2) 随机部分：80 位 -> 16 个 base32 字符（16 * 5 = 80 位）
    rand_bytes = os.urandom(10)  # 10 bytes = 80 bits
    rand_int = int.from_bytes(rand_bytes, 'big')
    rand_part = _to_base32(rand_int, 16)

    return f'{time_part}{rand_part}'


if __name__ == '__main__':
    for _ in range(3):
        print(new_time_sortable_id())
        # 01K6S531EC34X40WSFWE95C70S
        # 01K6T2HJYX5FS09NSVJN523SXQ
