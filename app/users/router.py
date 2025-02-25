from datetime import datetime
from fastapi import APIRouter, Depends, Response
from app.database import SessionManager
from app.users.auth import (
    authenticate_user,
    get_password_hash,
    create_acces_token,
    send_confirmation_email,
)
from app.users.dao import UserConfirmationDAO, UsersDAO
from app.users.dependencies import get_current_user
from app.users.models import UserConfirmations, Users
from app.users.schemas import SUserAuth
from app.exceptions import UserAlreadyExistsException, IncorrectEmailOrPasswordException
from app.users.auth import generate_confirmation_code

router = APIRouter(
    prefix="/auth",
    tags=["Auth & Пользователи"],
)


@router.post("/register")
async def register_user(user_data: SUserAuth):
    # Проверяем существование пользователя
    existing_user = await UsersDAO.find_one_or_none(email=user_data.email)
    if existing_user:
        raise UserAlreadyExistsException

    async with SessionManager() as session:
        # Хешируем пароль
        hashed_password = get_password_hash(user_data.password)

        # Создаем пользователя через DAO
        user_id = await UsersDAO.add(
            session=session, email=user_data.email, hashed_password=hashed_password
        )

        # Генерируем код подтверждения
        confirmation_code = await generate_confirmation_code()
        confirmation = UserConfirmations(
            user_id=user_id, confirmation_code=confirmation_code
        )
        # Создаем запись подтверждения через DAO
        await UserConfirmationDAO().add_confirmation(confirmation, session)

        # Отправляем email с подтверждением
        await send_confirmation_email(user_data.email, confirmation_code)

        await session.commit()

        return {
            "message": "User registered successfully. Please check your email for confirmation.",
            "user_id": user_id,
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
async def read_all_users(current_user: Users = Depends(get_current_user)):
    return await UsersDAO.find_all()


@router.delete("/delete")
async def delete_me(
    response: Response, currnet_user: Users = Depends(get_current_user)
):
    await UsersDAO.delete(id=currnet_user.id)
    response.delete_cookie("pdf_access_token")
    return {
        "message": "User deleted successfully",
        "user_id": currnet_user.id,
    }
