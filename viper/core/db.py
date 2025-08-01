from sqlalchemy import create_engine, text

# 创建 Engine，会自动使用连接池
engine = create_engine(
    "mysql+mysqldb://user:password@host:port/dbname",
    pool_size=10,  # 连接池大小
    max_overflow=20,  # 超过池大小后最多创建的连接数
    pool_recycle=3600,  # 连接多久后回收
    echo=True  # 输出执行的SQL，调试用
)

# 执行原生 SQL
with engine.connect() as conn:
    result = conn.execute(text("SELECT * FROM your_table WHERE id = :id"), {"id": 1})
    for row in result:
        print(row)
