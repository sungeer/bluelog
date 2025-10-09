

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

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    try:
        cursor.execute(create_sql)
        for sql in sql_indexes:
            cursor.execute(sql)

        conn.commit()
    finally:
        cursor.close()
        conn.close()

    with sqlite3.connect(DB_FILE) as conn:
        conn.execute('PRAGMA journal_mode=WAL;')


conn = sqlite3.connect(DB_FILE)
conn.execute('PRAGMA synchronous=NORMAL;')
conn.execute('PRAGMA busy_timeout=5000;')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()
try:
    cursor.execute(sql_str)
    upload_rows = cursor.fetchall()
finally:
    cursor.close()
    conn.close()


with self.p.db_lock:
    conn = sqlite3.connect(DB_FILE)
    conn.execute('PRAGMA synchronous=NORMAL;')
    conn.execute('PRAGMA busy_timeout=5000;')
    cursor = conn.cursor()
    try:
        cursor.execute(sql_str, params)
        conn.commit()
    except:
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()
