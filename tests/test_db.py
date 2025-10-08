from contextlib import suppress, contextmanager

import MySQLdb
from MySQLdb.cursors import DictCursor
from sqlalchemy.pool import QueuePool


def get_db_connect():
    db_connect = MySQLdb.connect(
        host='127.0.0.1',
        user='user',
        passwd='password',
        db='dbname',
        charset='utf8mb4',
        cursorclass=DictCursor,
    )
    return db_connect


db_pool = QueuePool(
    creator=get_db_connect,
    pool_size=5,
    max_overflow=10,
    timeout=30,
    recycle=1800,  # 30分钟回收，防止空闲断开
    pre_ping=True,
)


@contextmanager
def db_read():
    conn = None
    cursor = None
    try:
        conn = db_pool.connect()
        cursor = conn.cursor()
        yield cursor
    finally:
        with suppress(Exception):
            cursor and cursor.close()
        with suppress(Exception):
            conn and conn.close()


@contextmanager
def db_write(use_begin=False):
    conn = None
    cursor = None
    try:
        conn = db_pool.connect()
        if use_begin:
            conn.begin()
        cursor = conn.cursor()
        yield cursor
        conn.commit()
    except (Exception,):
        with suppress(Exception):
            conn and conn.rollback()
        raise
    finally:
        with suppress(Exception):
            cursor and cursor.close()
        with suppress(Exception):
            conn and conn.close()
