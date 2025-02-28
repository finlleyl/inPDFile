from datetime import datetime, timedelta, timezone
from sqlalchemy import (
    JSON,
    Boolean,
    Column,
    Computed,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    String,
    text,
)
from sqlalchemy.orm import relationship
from app.database import Base
from sqlalchemy.sql import func
from app.pdf.models import PdfDocuments


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_verified = Column(Boolean, nullable=False, default=False)
    registration_date = Column(DateTime, default=func.now())
    last_login_date = Column(DateTime, default=func.now())
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)

    # Связь один ко многим
    confirmations = relationship(
        "UserConfirmations", back_populates="user", cascade="all, delete-orphan"
    )
    documents = relationship(
        "PdfDocuments", back_populates="user", cascade="all, delete-orphan"
    )


class UserConfirmations(Base):
    __tablename__ = "user_confirmations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    confirmation_code = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(
        DateTime, default=lambda: datetime.utcnow() + timedelta(minutes=15)
    )
    is_used = Column(Boolean, default=False)

    user = relationship("Users", back_populates="confirmations")
