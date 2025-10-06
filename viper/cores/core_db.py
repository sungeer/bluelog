import MySQLdb
from MySQLdb.cursors import DictCursor
from sqlalchemy.pool import QueuePool


def create_db_connect():
    db_connect = MySQLdb.connect(
        host='127.0.0.1',
        user='root',
        passwd='admin',
        db='viper',
        charset='utf8mb4',
        cursorclass=DictCursor,
    )
    return db_connect


db_pool = QueuePool(
    creator=create_db_connect,
    pool_size=5,
    max_overflow=10,
    timeout=30,
    recycle=1800,  # 30分钟回收，防止空闲断开
    pre_ping=True,
)


def get_db_conn():
    db_conn = db_pool.connect()  # 从连接池中获取一个连接
    return db_conn
