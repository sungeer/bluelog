import sqlite3
import threading

from contextlib import suppress

db_file = ''

db_write_lock = threading.Lock()


def creat_db():
    create_sql = '''
        CREATE TABLE IF NOT EXISTS wei (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            run_id TEXT NOT NULL,
            tracking_no TEXT NOT NULL,
            created_at TEXT NOT NULL
        );
    '''

    sql_indexes = [
        'CREATE UNIQUE INDEX IF NOT EXISTS uniq_run_id ON wei(run_id);',
    ]

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    try:
        cursor.execute(create_sql)

        for sql in sql_indexes:
            cursor.execute(sql)
        conn.commit()
    finally:
        cursor.close()
        conn.close()

    with sqlite3.connect(db_file) as conn:
        conn.execute('PRAGMA journal_mode=WAL;')


def init_db_pragmas(conn):
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA synchronous=NORMAL;')
    conn.execute('PRAGMA journal_size_limit=134217728;')  # 限制WAL体积上限128MB
    conn.execute('PRAGMA busy_timeout=5000;')


def db_read():
    sql_str = ''
    conn = sqlite3.connect(db_file)
    init_db_pragmas(conn)
    cursor = conn.cursor()
    try:
        cursor.execute(sql_str)
        upload_rows = cursor.fetchall()
    finally:
        with suppress(Exception):
            cursor and cursor.close()
        with suppress(Exception):
            conn and conn.close()
    return upload_rows


def db_write():
    sql_str = ''
    params = ('a',)
    with db_write_lock:
        conn = sqlite3.connect(db_file)
        init_db_pragmas(conn)
        cursor = conn.cursor()
        try:
            cursor.execute(sql_str, params)
            conn.commit()
        except:
            conn.rollback()
            raise
        finally:
            with suppress(Exception):
                cursor and cursor.close()
            with suppress(Exception):
                conn and conn.close()
