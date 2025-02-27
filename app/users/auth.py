from datetime import datetime, timedelta, timezone
import random
from passlib.context import CryptContext
from jose import jwt
from pydantic import EmailStr
from app.config import settings

from app.users.dao import UsersDAO

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_passowrd) -> bool:
    return pwd_context.verify(plain_password, hashed_passowrd)


def create_acces_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=60)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, settings.ALGORITHM)
    return encoded_jwt


async def authenticate_user(email: EmailStr, password: str):
    user = await UsersDAO.find_one_or_none(email=email)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user


async def send_confirmation_email(email, code):
    pass


async def generate_confirmation_code() -> str:
    return str(random.randint(1, 9999)).zfill(4)
