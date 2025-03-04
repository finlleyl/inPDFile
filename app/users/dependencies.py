from datetime import datetime, timezone
from fastapi import Depends, Request
from jose import jwt, JWTError
from app.config import settings
from app.users.dao import UsersDAO
from app.users.models import Users
from app.exceptions import (
    AdminUserDoesNotExistException,
    BanUserException,
    NoVerificationException,
    TokenNotFoundException,
    TokenIncorrectFormatException,
    UserIsNotPresentException,
)


async def get_token(request: Request):
    token = request.cookies.get("pdf_access_token")
    if not token:
        raise TokenNotFoundException
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)

    except JWTError as e:
        raise TokenNotFoundException from e
    expire: str = payload.get("exp")
    if (not expire) or (datetime.now(timezone.utc).timestamp() > float(expire)):
        raise TokenIncorrectFormatException
    user_id: str = payload.get("sub")
    if not user_id:
        raise UserIsNotPresentException
    user = await UsersDAO.find_one_or_none(id=int(user_id))
    if not user:
        raise UserIsNotPresentException

    return user


async def get_current_user(current_user: Users = Depends(get_token)):
    if not current_user.is_verified:
        raise NoVerificationException
    if not current_user.is_active:
        raise BanUserException
    return current_user


async def get_current_admin_user(current_user: Users = Depends(get_current_user)):
    if not current_user.is_superuser:
        raise AdminUserDoesNotExistException

    return current_user
