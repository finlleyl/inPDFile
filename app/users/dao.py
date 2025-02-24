from app.dao.base import BaseDAO
from app.users.models import Users
from sqlalchemy.ext.asyncio import AsyncSession
from app.users.models import UserConfirmation
from app.database import async_session_maker
from typing import AsyncGenerator


class UsersDAO(BaseDAO):
    model = Users

    @classmethod
    async def add_confirmation(
        confirmation: UserConfirmation, session: AsyncSession
    ) -> UserConfirmation:
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
