from app.database import async_session_maker
from sqlalchemy import delete, insert, select


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
    async def add(cls, session=None, **data):
        if session is not None:
            query = insert(cls.model).values(**data).returning(cls.model.id)
            result = await session.execute(query)
            return result.scalar_one()

        async with async_session_maker() as session:
            query = insert(cls.model).values(**data).returning(cls.model.id)
            result = await session.execute(query)
            await session.commit()
            return result.scalar_one()

    @classmethod
    async def delete(cls, **data):
        async with async_session_maker() as session:
            query = delete(cls.model).filter_by(**data)
            await session.execute(query)
            await session.commit()
