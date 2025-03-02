from app.dao.base import BaseDAO
from sqlalchemy.ext.asyncio import AsyncSession
from app.pdf.models import PdfDocuments, PdfProcessingHistory
from app.database import async_session_maker
from typing import AsyncGenerator


class PdfDocumentsDAO(BaseDAO):
    model = PdfDocuments


class PdfProcessingHistoryDAO(BaseDAO):
    model = PdfProcessingHistory