import sqlite3
import threading
import time
from contextlib import contextmanager

DB_PATH = "app.db"

# 全局写锁：确保应用内所有写操作串行化（仅进程内有效）
write_lock = threading.Lock()


def get_connection(db_path=DB_PATH):
    # check_same_thread=False 允许将同一连接用于不同线程（谨慎使用）
    # 如果你打算每个线程独立连接，则保留默认 True，并在线程内创建并持有连接。
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    apply_pragmas(conn)
    return conn


def apply_pragmas(conn):
    # 根据你的桌面客户端推荐配置
    conn.execute("PRAGMA journal_mode=WAL;")  # WAL 模式
    conn.execute("PRAGMA synchronous=FULL;")  # 强一致性
    conn.execute("PRAGMA wal_autocheckpoint=8000;")  # 约 32MB（4KB页）
    conn.execute("PRAGMA journal_size_limit=268435456;")  # 256MB
    conn.execute("PRAGMA cache_size=-32768;")  # ≈128MB（4KB页）；可改 -65536
    conn.execute("PRAGMA temp_store=MEMORY;")
    conn.execute("PRAGMA mmap_size=268435456;")  # 256MB
    conn.execute("PRAGMA busy_timeout=5000;")  # 5s，增强健壮性


def init_schema(conn):
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


@contextmanager
def write_tx(conn):
    # 使用全局写锁 + IMMEDIATE 事务，避免写锁争用
    with write_lock:
        try:
            conn.execute("BEGIN IMMEDIATE;")
            yield
            conn.execute("COMMIT;")
        except Exception:
            conn.execute("ROLLBACK;")
            raise


def insert_operation(conn, plc_id, op_type, payload=None):
    with write_tx(conn):
        conn.execute(
            "INSERT INTO op_log (plc_id, op_type, payload) VALUES (?, ?, ?)",
            (plc_id, op_type, payload),
        )


def bulk_insert_operations(conn, rows):
    # rows: iterable of (plc_id, op_type, payload)
    with write_tx(conn):
        conn.executemany(
            "INSERT INTO op_log (plc_id, op_type, payload) VALUES (?, ?, ?)",
            rows
        )


def query_recent(conn, plc_id=None, limit=50):
    if plc_id:
        sql = """
            SELECT id, plc_id, op_type, payload, created_at
            FROM op_log
            WHERE plc_id = ?
            ORDER BY created_at DESC
            LIMIT ?
        """
        args = (plc_id, limit)
    else:
        sql = """
            SELECT id, plc_id, op_type, payload, created_at
            FROM op_log
            ORDER BY created_at DESC
            LIMIT ?
        """
        args = (limit,)

    cur = conn.execute(sql, args)
    rows = cur.fetchall()
    # Row 支持字典式访问
    return [dict(r) for r in rows]


def manual_checkpoint(conn, mode="TRUNCATE"):
    # 在空闲期可主动 checkpoint，保持 -wal 文件小
    # mode: PASSIVE | FULL | RESTART | TRUNCATE
    conn.execute(f"PRAGMA wal_checkpoint({mode});")


def main():
    conn = get_connection()
    init_schema(conn)

    # 模拟每2秒产生的多条写入：合并为一次事务
    for t in range(3):
        rows = [
            ("PLC-A", "START", '{"speed":120}'),
            ("PLC-A", "STATE", '{"ok":true}'),
            ("PLC-B", "ALARM", '{"code":42}'),
            ("PLC-C", "STOP", '{"reason":"manual"}'),
        ]
        bulk_insert_operations(conn, rows)
        print(f"batch {t} inserted {len(rows)} rows")
        time.sleep(2)

    # 查询最近记录
    recent = query_recent(conn, plc_id="PLC-A", limit=10)
    for r in recent:
        print(r)

    # 手动 checkpoint（可在应用空闲时调用）
    manual_checkpoint(conn, "TRUNCATE")

    conn.close()


if __name__ == "__main__":
    main()
