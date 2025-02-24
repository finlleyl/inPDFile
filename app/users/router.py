from datetime import datetime, timedelta, timezone
import uuid
from fastapi import APIRouter, Depends, Response
from app.database import SessionManager
from app.users.auth import (
    authenticate_user,
    get_password_hash,
    create_acces_token,
    send_confirmation_email,
)
from app.users.dao import UsersDAO
from app.users.dependencies import get_current_admin_user, get_current_user
from app.users.models import UserConfirmation, Users
from app.users.schemas import SUserAuth
from app.exceptions import UserAlreadyExistsException, IncorrectEmailOrPasswordException

router = APIRouter(
    prefix="/auth",
    tags=["Auth & Пользователи"],
)


@router.post("/register")
async def register_user(user_data: SUserAuth):
    async with SessionManager() as session:
        existing_user = await UsersDAO.find_one_or_none(email=user_data.email)
        if existing_user:
            raise UserAlreadyExistsException

        hashed_password = get_password_hash(user_data.password)
        new_user = Users(email=user_data.email, hashed_password=hashed_password)
        session.add(new_user)
        await session.flush()

        confirmation_code = str(uuid.uuid4())

        confirmation = UserConfirmation(
            user_id=new_user.id, confirmation_code=confirmation_code
        )
        session.add(confirmation)

        await send_confirmation_email(user_data.email, confirmation_code)

    return {
        "message": "User registered successfully. Please check your email for confirmation."
    }


@router.post("/confirm")
async def confirm_user(code: str):
    confirmation = await UsersDAO.find_confirmation(code=code)
    if not confirmation:
        raise ConfirmationDoesNotExistException
    if confirmation.is_used:
        raise ConfirmationAlreadyUsed
    if confirmation.expires_at < datetime.utcnow():
        raise ConfirmationExpiredException
    await UsersDAO.confirm_user(confirmation.user_id)
    return True


@router.post("/login")
async def login(response: Response, user_data: SUserAuth):
    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        raise IncorrectEmailOrPasswordException
    acces_token = create_acces_token({"sub": str(user.id)})
    response.set_cookie("pdf_access_token", acces_token, httponly=True)
    return {"access_token": acces_token}


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("pdf_access_token")
    return True


@router.get("/me")
async def read_me(current_user: Users = Depends(get_current_user)):
    return current_user


@router.get("/all_users")
async def read_all_users(current_user: Users = Depends(get_current_admin_user)):
    return await UsersDAO.find_all()
