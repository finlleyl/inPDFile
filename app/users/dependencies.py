from datetime import datetime, timezone
from fastapi import Depends, Request
from jose import jwt, JWTError
from app.config import settings
from app.users.dao import UsersDAO
from app.users.models import Users
from app.exceptions import (
    TokenNotFoundException,
    TokenIncorrectFormatException,
    UserIsNotPresentException,
)


def get_token(request: Request) -> dict:
    token = request.cookies.get("pdf_access_token")
    if not token:
        raise TokenNotFoundException
    return token


async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)

    except JWTError:
        raise TokenNotFoundException
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


async def get_current_admin_user(current_user: Users = Depends(get_current_user)):
    # if current_user.role != "admin":
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    return current_user
