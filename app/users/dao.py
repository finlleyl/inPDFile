from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.users.models import Users, UserConfirmations


class UsersDAO(BaseDAO):
    model = Users


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
