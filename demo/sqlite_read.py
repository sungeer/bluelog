import sqlite3
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from contextlib import contextmanager
import time

DB_PATH = "app.db"
WRITE_LOCK = threading.Lock()  # 串行化写


def make_conn():
    conn = sqlite3.connect(
        DB_PATH,
        timeout=5.0,  # busy_timeout 等价（秒）
        isolation_level=None,  # autocommit，手动控制事务
        check_same_thread=False
    )
    conn.row_factory = sqlite3.Row
    apply_pragmas(conn)
    return conn


def apply_pragmas(conn):
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA synchronous=FULL;")  # 服务器可用 NORMAL
    conn.execute("PRAGMA wal_autocheckpoint=8000;")
    conn.execute("PRAGMA journal_size_limit=268435456;")
    conn.execute("PRAGMA cache_size=-32768;")  # ≈128MB；如读连接多可适当调小
    conn.execute("PRAGMA temp_store=MEMORY;")
    conn.execute("PRAGMA mmap_size=268435456;")
    conn.execute("PRAGMA busy_timeout=5000;")


def init_schema():
    conn = make_conn()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS op_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            plc_id TEXT NOT NULL,
            op_type TEXT NOT NULL,
            payload TEXT,
            created_at DATETIME DEFAULT (strftime('%Y-%m-%d %H:%M:%f','now'))
        );
    """)
    conn.execute("CREATE INDEX IF NOT EXISTS idx_oplog_created ON op_log(created_at);")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_oplog_plc ON op_log(plc_id, created_at);")
    conn.close()


@contextmanager
def write_tx(conn):
    with WRITE_LOCK:
        try:
            conn.execute("BEGIN IMMEDIATE;")
            yield
            conn.execute("COMMIT;")
        except Exception:
            conn.execute("ROLLBACK;")
            raise


def write_batch(rows):
    """rows: iterable of (plc_id, op_type, payload)"""
    conn = make_conn()
    try:
        with write_tx(conn):
            conn.executemany(
                "INSERT INTO op_log (plc_id, op_type, payload) VALUES (?, ?, ?)",
                rows
            )
    finally:
        conn.close()


def read_task(query_args):
    """单个读任务：为该线程创建并持有一个独立连接"""
    conn = make_conn()
    try:
        plc_id, limit = query_args
        if plc_id is None:
            sql = """SELECT id, plc_id, op_type, payload, created_at
                     FROM op_log ORDER BY created_at DESC LIMIT ?"""
            args = (limit,)
        else:
            sql = """SELECT id, plc_id, op_type, payload, created_at
                     FROM op_log WHERE plc_id = ? ORDER BY created_at DESC LIMIT ?"""
            args = (plc_id, limit)
        cur = conn.execute(sql, args)
        rows = cur.fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def manual_checkpoint():
    conn = make_conn()
    try:
        conn.execute("PRAGMA wal_checkpoint(TRUNCATE);")
    finally:
        conn.close()


def main():
    init_schema()

    # 模拟写入（串行）
    write_batch([
        ("PLC-A", "START", '{"speed":120}'),
        ("PLC-A", "STATE", '{"ok":true}'),
        ("PLC-B", "ALARM", '{"code":42}'),
        ("PLC-C", "STOP", '{"reason":"manual"}'),
    ])

    # 并发读：最多同时 8 个
    queries = [
        ("PLC-A", 10),
        ("PLC-B", 10),
        (None, 10),
        ("PLC-C", 10),
        ("PLC-A", 5),
        ("PLC-B", 5),
        ("PLC-C", 5),
        (None, 20),
        # 再多也会排队，因为 max_workers=8
    ]

    t0 = time.time()
    results = []
    with ThreadPoolExecutor(max_workers=8) as pool:
        futures = [pool.submit(read_task, q) for q in queries]
        for fut in as_completed(futures):
            results.append(fut.result())
    t1 = time.time()

    print(f"Executed {len(queries)} read tasks concurrently (<=8). Time: {t1 - t0:.3f}s")
    print(f"Sample result count of first task: {len(results[0])}")

    # 空闲时可做 checkpoint
    manual_checkpoint()


if __name__ == "__main__":
    main()
