from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, AsyncAttrs, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, declared_attr
from app.config import settings
from app.logger import logger

if settings.MODE == "TEST":
    DATABASE_URL = settings.TEST_DATABASE_URL
    DATABASE_PARAMS = {"poolclass": NullPool}
else:
    DATABASE_URL = settings.DATABASE_URL
    DATABASE_PARAMS = {}


try:
    engine = create_async_engine(DATABASE_URL, **DATABASE_PARAMS)
    async_session_maker = async_sessionmaker(engine, expire_on_commit=False)
except Exception as e:
    logger.error(f"Failed to create database engine: {e}")
    raise


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"


class SessionManager:
    def __init__(self):
        self.session = None

    async def __aenter__(self):
        self.session = async_session_maker()
        return self.session

    async def __aexit__(self, exc_type, exc_value, traceback):
        try:
            if exc_type:
                await self.session.rollback()
            else:
                await self.session.commit()
        finally:
            await self.session.close()
