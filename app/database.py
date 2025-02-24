from sqlalchemy.ext.asyncio import create_async_engine, AsyncAttrs,async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, declared_attr 
from app.config import settings


engine = create_async_engine(settings.DATABASE_URL)

async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"
