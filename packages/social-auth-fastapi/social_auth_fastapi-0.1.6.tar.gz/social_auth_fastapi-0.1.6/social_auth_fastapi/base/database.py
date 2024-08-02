import sys

from pydantic import PostgresDsn, MySQLDsn
from pydantic_core import Url
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from .errors import ServerError

postgres_allowed_schemes = [
    'postgres',
    'postgresql',
    'postgresql+asyncpg',
    'postgresql+pg8000',
    'postgresql+psycopg',
    'postgresql+psycopg2',
    'postgresql+psycopg2cffi',
    'postgresql+py-postgresql',
    'postgresql+pygresql',
]

mysql_allowed_schemes = [
    'mysql',
    'mysql+mysqlconnector',
    'mysql+aiomysql',
    'mysql+asyncmy',
    'mysql+mysqldb',
    'mysql+pymysql',
    'mysql+cymysql',
    'mysql+pyodbc',
]


def validate_database_dns(url: str):
    url = Url(url)
    if url.scheme in postgres_allowed_schemes:
        dsn = PostgresDsn.build(
            scheme='postgresql+asyncpg',
            username=url.username,
            password=url.password,
            host=url.host,
            port=url.port,
            path=url.path[1:],
        )
    elif url.scheme in mysql_allowed_schemes:
        dsn = MySQLDsn.build(
            scheme='mysql+asyncmy',
            username=url.username,
            password=url.password,
            host=url.host,
            port=url.port,
            path=url.path[1:],
        )
    else:
        raise ServerError(msg='SQLDsn not allowed_schemes')

    return str(dsn)


def create_engine_and_session(url: str):
    try:
        # Database engine
        url = validate_database_dns(url)
        engine = create_async_engine(url, future=True, pool_pre_ping=True)
    except Exception as e:
        sys.exit()
    else:
        db_session = async_sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
        return engine, db_session
