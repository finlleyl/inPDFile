from datetime import datetime
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
)
from sqlalchemy.orm import relationship
from app.database import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_verified = Column(Boolean, nullable=False, default=False)
    confirmations = relationship("UserConfirmation", back_populates="user")
    registration_date = Column(DateTime, default=datetime.now(datetime.timezone.utc))
    last_login_date = Column(DateTime, default=datetime.now(datetime.timezone.utc))
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)


class UserConfirmation(Base):
    __tablename__ = "user_confirmations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    confirmation_code = Column(
        String, unique=True, index=True, nullable=False
    )  # уникальный код подтверждения, который будет отправлен пользователю на email.
    created_at = Column(DateTime, default=datetime.now(datetime.timezone.utc))
    expires_at = Column(DateTime, nullable=False)
    is_used = Column(Boolean, default=False)

    user = relationship("User", back_populates="confirmations")
