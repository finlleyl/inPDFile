from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update
from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.users.models import Users, UserConfirmations
from app.logger import logger


class UsersDAO(BaseDAO):
    model = Users

    @classmethod
    async def confirm_user(cls, u_id: int) -> bool:
        try:
            async with async_session_maker() as session:
                query1 = (
                    update(cls.model).where(Users.id == u_id).values(is_verified=True)
                )
                query2 = (
                    update(UserConfirmations)
                    .where(UserConfirmations.user_id == u_id)
                    .values(is_used=True)
                )
                result = await session.execute(query1)
                await session.execute(query2)
                await session.commit()
                return result
        except Exception as e:
            logger.error(
                f"Error in find_one_or_none for {cls.model.__name__}",
                extra={"id": u_id, "error": str(e)},
            )
            raise


class UserConfirmationDAO(BaseDAO):
    model = UserConfirmations

    @classmethod
    async def add_confirmation(
        cls, confirmation: UserConfirmations, session: AsyncSession
    ) -> UserConfirmations:
        """
        Добавляет объект подтверждения пользователя в базу данных с использованием переданной сессии.
        """
        session.add(confirmation)
        await session.flush()
        return confirmation

    async def get_session() -> AsyncGenerator[AsyncSession, None]:
        async with async_session_maker() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise
