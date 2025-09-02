import time
from datetime import datetime


def get_now(format_type: str) -> str:
    now = datetime.now()
    format_map = {
        'datetime': lambda: now.strftime('%Y-%m-%d %H:%M:%S'),
        'date': lambda: now.strftime('%Y-%m-%d'),
        'time': lambda: now.strftime('%H:%M:%S'),
        'timestamp': lambda: str(int(time.time() * 1000)),  # 毫秒级时间戳
        'filename': lambda: now.strftime('%Y%m%d_%H%M%S'),
        'logfile': lambda: now.strftime('%Y-%m-%d_%H:%M:%S.%f'),
    }
    func = format_map.get(format_type, '')
    if not func:
        raise ValueError(f'Unsupported format_type: {format_type}')
    return func()


# 时间戳 转 日期
def timestamp_to_datetime(ts: int) -> str:
    return datetime.fromtimestamp(ts / 1000).strftime('%Y-%m-%d %H:%M:%S')


if __name__ == '__main__':
    print(get_now('datetime'))  # 2025-07-13 21:33:12
    print(get_now('date'))  # 2025-07-13
    print(get_now('time'))  # 21:33:12
    print(get_now('timestamp'))  # 1713028392000
    print(get_now('filename'))  # 20250713_213312
    print(get_now('logfile'))  # 2025-07-23_10:06:20.127633

    print(timestamp_to_datetime(1713028392000))  # 2024-07-14 01:13:12
