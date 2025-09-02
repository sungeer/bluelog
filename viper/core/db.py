from sqlalchemy.ext.asyncio import create_async_engine

DATABASE_URL = "mysql+asyncmy://user:password@localhost:3306/dbname"

engine = create_async_engine(
    DATABASE_URL,
    max_overflow=20,  # 最大溢出
    pool_recycle=1800,
)
