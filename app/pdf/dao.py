from datetime import date
from app.database import engine, async_session_maker
from sqlalchemy import and_, func, insert, select
from app.dao.base import BaseDAO


class PdfDAO(BaseDAO):
    model = Pdf

    @classmethod
    async def add():
        
        async with async_session_maker() as session:
            pass
