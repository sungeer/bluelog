import os
import sqlite3
import threading
from queue import LifoQueue, Empty
from contextlib import contextmanager

from flask import Flask, jsonify, request, g, abort

DB_PATH = os.environ.get("DB_PATH", "news.db")

# 读连接池：限制同时最多 8 个活跃读
READ_POOL_SIZE = int(os.environ.get("READ_POOL_SIZE", 8))
_read_pool = LifoQueue(maxsize=READ_POOL_SIZE)

# 写入串行化
WRITE_LOCK = threading.Lock()

app = Flask(__name__)


def connect_db():
    # 每个连接应用服务器场景推荐 PRAGMA
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    apply_server_pragmas(conn)
    return conn


def apply_server_pragmas(conn):
    # 服务器（读多写少）配置建议
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA synchronous=NORMAL;")  # 性能/可靠性折中
    conn.execute("PRAGMA wal_autocheckpoint=16000;")  # 约 64MB（4KB页），可 12000–20000
    conn.execute("PRAGMA journal_size_limit=536870912;")  # 512MB 上限
    conn.execute("PRAGMA cache_size=-65536;")  # ≈256MB，读连接可酌情调小，如 -16384=64MB
    conn.execute("PRAGMA temp_store=MEMORY;")
    conn.execute("PRAGMA mmap_size=1073741824;")  # 1GB，可按 DB 体量与内存调整
    conn.execute("PRAGMA busy_timeout=5000;")


def init_schema():
    conn = connect_db()
    try:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS news (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                body TEXT NOT NULL,
                tags TEXT,
                hot_score REAL DEFAULT 0,
                published_at DATETIME NOT NULL DEFAULT (strftime('%Y-%m-%d %H:%M:%f','now'))
            );
        """)
        conn.execute("CREATE INDEX IF NOT EXISTS idx_news_pub ON news(published_at DESC);")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_news_hot ON news(hot_score DESC, published_at DESC);")
        # 可选：FTS5 全文索引（需要在同库启用，可做虚表镜像）
        # conn.execute("CREATE VIRTUAL TABLE IF NOT EXISTS news_fts USING fts5(title, body, content='news', content_rowid='id');")
        # 触发器维护 FTS 省略，这里聚焦 PRAGMA 与并发模型
    finally:
        conn.close()


def _populate_read_pool():
    # 预创建读连接，减少请求时的建连开销
    for _ in range(READ_POOL_SIZE):
        _read_pool.put(connect_db())


@app.before_first_request
def boot():
    init_schema()
    _populate_read_pool()


@contextmanager
def read_conn():
    """从读池借一个连接；请求结束归还。池满且无可用时会阻塞到 timeout。"""
    try:
        conn = _read_pool.get(timeout=5.0)
    except Empty:
        # 极端情况下也可以临时新建一个连接兜底，但这里选择 503 显式限流
        abort(503, description="Too many concurrent reads")
    try:
        yield conn
    finally:
        _read_pool.put(conn)


@contextmanager
def write_tx():
    """全局写锁 + IMMEDIATE 事务，串行化写入，减少 BUSY。"""
    with WRITE_LOCK:
        conn = connect_db()
        try:
            conn.execute("BEGIN IMMEDIATE;")
            yield conn
            conn.execute("COMMIT;")
        except Exception:
            conn.execute("ROLLBACK;")
            raise
        finally:
            conn.close()


@app.get("/health")
def health():
    return {"ok": True}


@app.get("/news")
def list_news():
    # 查询参数：order=hot|time, limit, offset, tag
    order = request.args.get("order", "time")
    limit = min(int(request.args.get("limit", 20)), 100)
    offset = max(int(request.args.get("offset", 0)), 0)
    tag = request.args.get("tag")

    if order == "hot":
        order_by = "hot_score DESC, published_at DESC"
    else:
        order_by = "published_at DESC"

    sql = f"""
        SELECT id, title, hot_score, published_at
        FROM news
        WHERE (? IS NULL OR (tags IS NOT NULL AND tags LIKE '%' || ? || '%'))
        ORDER BY {order_by}
        LIMIT ? OFFSET ?
    """
    args = (tag, tag, limit, offset)

    with read_conn() as conn:
        rows = conn.execute(sql, args).fetchall()
        return jsonify([dict(r) for r in rows])


@app.get("/news/<int:news_id>")
def get_news(news_id: int):
    with read_conn() as conn:
        row = conn.execute(
            "SELECT id, title, body, tags, hot_score, published_at FROM news WHERE id = ?",
            (news_id,)
        ).fetchone()
        if not row:
            abort(404)
        return jsonify(dict(row))


@app.post("/news")
def create_news():
    data = request.get_json(silent=True) or {}
    title = data.get("title")
    body = data.get("body")
    tags = data.get("tags")
    if not title or not body:
        abort(400, description="title and body are required")

    with write_tx() as conn:
        cur = conn.execute(
            "INSERT INTO news (title, body, tags) VALUES (?, ?, ?)",
            (title, body, tags)
        )
        new_id = cur.lastrowid
    return jsonify({"id": new_id}), 201


@app.post("/news/<int:news_id>/hot")
def update_hot(news_id: int):
    data = request.get_json(silent=True) or {}
    delta = float(data.get("delta", 0))
    with write_tx() as conn:
        cur = conn.execute(
            "UPDATE news SET hot_score = hot_score + ? WHERE id = ?",
            (delta, news_id)
        )
        if cur.rowcount == 0:
            abort(404)
    return jsonify({"ok": True})


@app.post("/admin/checkpoint")
def manual_checkpoint():
    # 低峰调用：帮助控制 -wal 文件大小与恢复时间
    with write_tx() as conn:
        # 使用 PASSIVE/FULL/RESTART/TRUNCATE；此处 TRUNCATE
        conn.execute("PRAGMA wal_checkpoint(TRUNCATE);")
    return jsonify({"ok": True})


if __name__ == "__main__":
    # 在开发环境下使用 Flask 内置服务器；生产请使用 gunicorn/uwsgi 等 WSGI 容器
    # 示例：gunicorn -w 4 -k gthread --threads 16 app:app
    app.run(host="0.0.0.0", port=5000, debug=True)
