from app.dao.base import BaseDAO
from app.pdf.models import PdfDocuments, PdfProcessingHistory


class PdfDocumentsDAO(BaseDAO):
    model = PdfDocuments


class PdfProcessingHistoryDAO(BaseDAO):
    model = PdfProcessingHistory
