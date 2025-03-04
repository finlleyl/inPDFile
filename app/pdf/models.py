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
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.database import Base


class PdfDocuments(Base):
    __tablename__ = "pdf_documents"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    file_name: Mapped[str] = mapped_column(String, nullable=False)
    file_path: Mapped[str] = mapped_column(String, nullable=False)
    file_size: Mapped[int] = mapped_column(Integer, nullable=False)
    upload_date: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow
    )
    status: Mapped[str] = mapped_column(String, default="в очереди", nullable=False)
    classification: Mapped[str] = mapped_column(String, nullable=False)
    document_metadata: Mapped[JSON] = mapped_column(JSON, nullable=False)
    document_type: Mapped[str] = mapped_column(String, nullable=False)
    has_signature: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_stamp: Mapped[bool] = mapped_column(Boolean, nullable=False)

    # Связь с пользователем (многие к одному)
    user = relationship("Users", back_populates="documents")

    # Связь с историей обработки (один ко многим)
    processing_history = relationship(
        "PdfProcessingHistory", back_populates="document", cascade="all, delete-orphan"
    )


class PdfProcessingHistory(Base):
    __tablename__ = "pdf_processing_history"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    document_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("pdf_documents.id", ondelete="CASCADE"), nullable=False
    )
    status: Mapped[str] = mapped_column(String, default="в очереди", nullable=False)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow
    )
    log: Mapped[Text] = mapped_column(Text, nullable=False)

    # Связь с документом (многие к одному)
    document = relationship("PdfDocuments", back_populates="processing_history")
