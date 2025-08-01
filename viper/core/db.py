from sqlalchemy import create_engine

engine = create_engine(
    'mysql+mysqldb://user:password@host:port/dbname',
    pool_recycle=1800,
)
