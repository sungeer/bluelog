import sqlite3
import threading

from contextlib import suppress

db_file = ''

db_write_lock = threading.Lock()  # 无需事务


def creat_db():
    create_sql = '''
        CREATE TABLE IF NOT EXISTS op_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            plc_id TEXT NOT NULL,
            op_type TEXT NOT NULL,
            payload TEXT,
            created_at TEXT NOT NULL
        );
    '''

    sql_indexes = [
        'CREATE UNIQUE INDEX IF NOT EXISTS uniq_plc_id ON op_log(plc_id);',
        'CREATE INDEX IF NOT EXISTS idx_oplog_created ON op_log(created_at);',
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
    sql_str = '''
        SELECT id, plc_id, op_type, payload, created_at
        FROM op_log
        ORDER BY created_at DESC
    '''
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
    sql_str = '''
        INSERT INTO op_log (plc_id, op_type, payload)
        VALUES (?, ?, ?)
    '''
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


def db_write_many():
    sql_str = '''
        INSERT INTO op_log (plc_id, op_type, payload)
        VALUES (?, ?, ?)
    '''
    rows = [(1, "a"), (2, "b"), (3, "c")]
    with db_write_lock:
        conn = sqlite3.connect(db_file)
        init_db_pragmas(conn)
        cursor = conn.cursor()
        try:
            cursor.executemany(sql_str, rows)
            conn.commit()
        except:
            conn.rollback()
            raise
        finally:
            with suppress(Exception):
                cursor and cursor.close()
            with suppress(Exception):
                conn and conn.close()
