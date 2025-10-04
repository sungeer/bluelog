import time
from datetime import datetime


def wait_ms(ms=20):
    time.sleep(ms / 1000.0)
    return


def get_now_dt():
    now = datetime.now()
    return now.strftime('%Y-%m-%d %H:%M:%S')
