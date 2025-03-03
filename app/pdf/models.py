from datetime import datetime
from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    JSON,
    Boolean,
    Text,
)
from sqlalchemy.orm import relationship
from app.database import Base


class PdfDocuments(Base):
    __tablename__ = "pdf_documents"

    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    file_name = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    file_size = Column(Integer, nullable=False)
    upload_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    status = Column(String, default="в очереди", nullable=False)
    classification = Column(String, nullable=False)
    document_metadata = Column(JSON, nullable=False)
    document_type = Column(String, nullable=False)
    has_signature = Column(Boolean, nullable=False)
    has_stamp = Column(Boolean, nullable=False)

    # Связь с пользователем (многие к одному)
    user = relationship("Users", back_populates="documents")

    # Связь с историей обработки (один ко многим)
    processing_history = relationship(
        "PdfProcessingHistory", back_populates="document", cascade="all, delete-orphan"
    )


class PdfProcessingHistory(Base):
    __tablename__ = "pdf_processing_history"

    id = Column(Integer, primary_key=True, nullable=False)
    document_id = Column(
        Integer, ForeignKey("pdf_documents.id", ondelete="CASCADE"), nullable=False
    )
    status = Column(String, default="в очереди", nullable=False)
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow)
    log = Column(Text, nullable=False)

    # Связь с документом (многие к одному)
    document = relationship("PdfDocuments", back_populates="processing_history")
