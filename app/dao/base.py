from app.database import async_session_maker
from sqlalchemy import insert, select


class BaseDAO:
    model = None

    @classmethod
    async def find_one_or_none(cls, **filtered_by):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(**filtered_by)
            result = await session.execute(query)
            return result.mappings().one_or_none()

    @classmethod
    async def find_all(cls, **filtered_by):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(**filtered_by)
            result = await session.execute(query)
            return result.mappings().all()

    @classmethod
    async def add(cls, **data):
        async with async_session_maker() as session:
            query = insert(cls.model).values(**data).returning(cls.model.id)
            await session.execute(query)
            await session.commit()

    @classmethod
    async def delete(cls, **data):
        async with async_session_maker() as session:
            query = cls.model.delete().where(**data)
            await session.execute(query)
            await session.commit()
