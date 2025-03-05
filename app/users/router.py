from datetime import datetime
from fastapi import APIRouter, Depends, Response
from app.database import SessionManager
from app.tasks.tasks import send_registration_confirmation
from app.users.auth import authenticate_user, get_password_hash, create_acces_token
from app.users.dao import UserConfirmationDAO, UsersDAO
from app.users.dependencies import get_current_user, get_token
from app.users.models import UserConfirmations, Users
from app.users.schemas import SUserAuth
from app.exceptions import (
    BanUserException,
    ConfirmationEmailNotSentException,
    ConfirmationExpiredException,
    FiledUpdateVerificationException,
    IncorrectConfirmationCodeException,
    NoVerificationException,
    UserAlreadyExistsException,
    IncorrectEmailOrPasswordException,
    ConfirmationDoesNotExistException,
    ConfirmationAlreadyUsed,
)
from app.users.auth import generate_confirmation_code
from app.logger import logger

router = APIRouter(
    prefix="/auth",
    tags=["Auth & Пользователи"],
)


@router.post("/register")
async def register_user(user_data: SUserAuth, response: Response):
    try:
        existing_user = await UsersDAO.find_one_or_none(email=user_data.email)
        if existing_user:
            logger.warning(
                f"Registration attempt with existing email: {user_data.email}"
            )
            raise UserAlreadyExistsException

        async with SessionManager() as session:
            hashed_password = get_password_hash(user_data.password)
            user_id = await UsersDAO.add(
                session=session, email=user_data.email, hashed_password=hashed_password
            )

            confirmation_code = await generate_confirmation_code()
            confirmation = UserConfirmations(
                user_id=user_id, confirmation_code=confirmation_code
            )
            await UserConfirmationDAO().add_confirmation(confirmation, session)
            try:
                send_registration_confirmation.delay(user_data.email, confirmation_code)
            except Exception as e:
                logger.error(
                    "Error during sending confirmation email",
                    extra={"email": user_data.email, "error": str(e)},
                )
                raise ConfirmationEmailNotSentException from e

            await session.commit()
            logger.info(
                "New user registered successfully", extra={"email": user_data.email}
            )

            acces_token = create_acces_token({"sub": str(user_id)})
            response.set_cookie("pdf_access_token", acces_token, httponly=True)
            logger.info("User registered successfully", extra={"user_id": user_id})
            return {
                "message": "User registered successfully. Please check your email for confirmation.",
                "access_token": acces_token,
                "user_id": user_id,
            }

    except Exception as e:
        logger.error(
            "Error during user registration",
            extra={"email": user_data.email, "error": str(e)},
        )
        raise


@router.put("/confirm")
async def confirm_user(code: str, response: Response, user: Users = Depends(get_token)):
    try:
        user_confirmation: UserConfirmations = (
            await UserConfirmationDAO.find_one_or_none(
                confirmation_code=code, user_id=user.id
            )
        )  # из бд
        if not user_confirmation:
            logger.warning("Confirmation attempt with non-existent code: {code}")
            raise ConfirmationDoesNotExistException
        if user_confirmation.is_used:
            logger.warning("Confirmation attempt with used code: {code}")
            raise ConfirmationAlreadyUsed
        if user_confirmation.expires_at < datetime.utcnow():
            logger.warning("Confirmation attempt with expired code: {code}")
            raise ConfirmationExpiredException
        if user_confirmation.confirmation_code == code:
            update_confirm = await UsersDAO.confirm_user(user_confirmation.user_id)
        else:
            logger.error("Confirmation attempt with incorrect code: {code}")
            raise IncorrectConfirmationCodeException
        if not update_confirm:
            logger.warrning(
                "User confirmation failed", extra={"user_id": user_confirmation.user_id}
            )
            raise FiledUpdateVerificationException
        logger.info(
            "User confirmed successfully", extra={"user_id": user_confirmation.user_id}
        )
        return {
            "message": "User confirmed successfully. Welcome.",
            "user_id": user_confirmation.user_id,
        }
    except Exception as e:
        logger.error(
            "Error during user confirmation", extra={"code": code, "error": str(e)}
        )
        raise


@router.post("/login")
async def login(response: Response, user_data: SUserAuth):
    try:
        user = await authenticate_user(user_data.email, user_data.password)
        if not user:
            logger.warning("Failed login attempt", extra={"email": user_data.email})
            raise IncorrectEmailOrPasswordException
        if not user.is_verified:
            logger.warning("Failed login attempt", extra={"email": user_data.email})
            raise NoVerificationException
        if not user.is_active:
            logger.warning("Failed login attempt", extra={"email": user_data.email})
            raise BanUserException

        acces_token = create_acces_token({"sub": str(user.id)})
        response.set_cookie("pdf_access_token", acces_token, httponly=True)
        logger.info("User logged in successfully", extra={"user_id": user.id})
        return {"access_token": acces_token}
    except Exception as e:
        logger.error(
            "Error during login", extra={"email": user_data.email, "error": str(e)}
        )
        raise


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("pdf_access_token")
    return True


@router.get("/me")
async def read_me(current_user: Users = Depends(get_current_user)):
    return current_user


@router.get("/all_users")
async def read_all_users(_current_user: Users = Depends(get_current_user)):
    return await UsersDAO.find_all()


@router.delete("/delete")
async def delete_me(response: Response, current_user: Users = Depends(get_token)):
    await UsersDAO.delete(id=current_user.id)
    response.delete_cookie("pdf_access_token")
    return {
        "user_id": current_user.id,
        "message": "User deleted successfully",
    }
