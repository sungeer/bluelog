from sqlalchemy import create_engine

DATABASE_URL = 'mysql+mysqldb://user:password@host:port/dbname'

engine = create_engine(
    DATABASE_URL,
    pool_recycle=1800,
)
