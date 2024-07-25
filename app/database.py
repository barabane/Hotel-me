from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from config import settings

if settings.MODE == "TEST":
    DB_URL = settings.TEST_DATABASE_URL
    DATABASE_PARAMS = {"poolclass": NullPool}
else:
    DB_URL = settings.DATABASE_URL
    DATABASE_PARAMS = {}

engine = create_async_engine(url=DB_URL, **DATABASE_PARAMS)
engine_nullpool = create_async_engine(
    url=settings.DATABASE_URL, **{"poolclass": NullPool})

async_session_maker = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False)

nullpool_session_maker = sessionmaker(
    engine_nullpool, class_=AsyncSession, expire_on_commit=False
)


class Base(DeclarativeBase):
    pass
