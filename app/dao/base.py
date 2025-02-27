from app.database import async_session_maker
from sqlalchemy import delete, insert, select
from app.logger import logger


class BaseDAO:
    model = None

    @classmethod
    async def find_one_or_none(cls, **filtered_by):
        try:
            async with async_session_maker() as session:
                query = select(cls.model.__table__.columns).filter_by(**filtered_by)
                result = await session.execute(query)
                return result.mappings().one_or_none()
        except Exception as e:
            logger.error(
                f"Error in find_one_or_none for {cls.model.__name__}",
                extra={"filter": filtered_by, "error": str(e)},
            )
            raise

    @classmethod
    async def find_all(cls, **filtered_by):
        try:
            async with async_session_maker() as session:
                query = select(cls.model.__table__.columns).filter_by(**filtered_by)
                result = await session.execute(query)
                return result.mappings().all()
        except Exception as e:
            logger.error(
                f"Error in find_all for {cls.model.__name__}",
                extra={"filter": filtered_by, "error": str(e)},
            )
            raise

    @classmethod
    async def add(cls, session=None, **data):
        try:
            if session is not None:
                query = insert(cls.model).values(**data).returning(cls.model.id)
                result = await session.execute(query)
                logger.info(f"Added new {cls.model.__name__}", extra={"data": data})
                return result.scalar_one()

            async with async_session_maker() as session:
                query = insert(cls.model).values(**data).returning(cls.model.id)
                result = await session.execute(query)
                await session.commit()
                logger.info(f"Added new {cls.model.__name__}", extra={"data": data})
                return result.scalar_one()
        except Exception as e:
            logger.error(
                f"Error adding {cls.model.__name__}",
                extra={"data": data, "error": str(e)},
            )
            raise

    @classmethod
    async def delete(cls, **data):
        try:
            async with async_session_maker() as session:
                query = delete(cls.model).filter_by(**data)
                result = await session.execute(query)
                await session.commit()
                deleted_count = result.rowcount
                logger.info(
                    f"Deleted {cls.model.__name__} records",
                    extra={"filter": data, "count": deleted_count},
                )
                return deleted_count
        except Exception as e:
            logger.error(
                f"Error deleting {cls.model.__name__}",
                extra={"filter": data, "error": str(e)},
            )
            raise
