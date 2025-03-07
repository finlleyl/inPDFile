from httpx import AsyncClient
import pytest

from app.users.dao import UserConfirmationDAO, UsersDAO


@pytest.mark.parametrize(
    "email,password,status_code",
    [
        ("kot@gmail.com", "123456", 200),
        ("kot@gmail.com", "123456", 409),
        ("kot@gmail.com", "12343561234", 409),
        ("ne-email", "123456", 422),
        ("kot1@gmail.com", "1", 422),
        ("kot1@gmail.com", "123456789111111234451234", 422),
    ],
)
async def test_register_user(email, password, status_code, ac: AsyncClient):
    """
    Тестирование эндпоинта регистрации пользователя.

    Проверяет, что эндпоинт возвращает ожидаемый статус код в зависимости от введенных данных.

    Параметры:
    email (str): email пользователя
    password (str): пароль пользователя
    status_code (int): ожидаемый статус код
    ac (AsyncClient): асинхронный клиент для отправки запросов

    ("kot@gmail.com", "123456", 200) - Успешный вход
    ("kot@gmail.com", "123456", 409) - Регистрация существующего пользователя
    ("kot@gmail.com", "12343561234", 409) - Неправильный пароль
    ("ne-email", "123456", 422) - Неправильный email
    ("kot1@gmail.com", "1", 422) - Короткий пароль < 6 символов
    ("kot1@gmail.com", "123456789111111234451234", 422) Длинный пароль > 20 симоволов

    """
    response = await ac.post(
        "auth/register",
        json={
            "email": email,
            "password": password,
        },
    )
    user = await UsersDAO.find_one_or_none(email=email)
    if user:
        assert response.status_code == status_code
        user_confirmation = await UserConfirmationDAO().find_all(user_id=user.id)
        assert user_confirmation is not None


# @pytest.mark.parametrize()
# async def test_confirm()


@pytest.mark.parametrize(
    "email,password,status_code",
    [
        ("testt@example.com", "string", 200),
        ("testt@example.com", "string1", 401),
        ("user1@example.com", "string", 401),
        ("", "", 422),
    ],
)
async def test_login(email, password, status_code, ac: AsyncClient):
    response = await ac.post(
        "auth/login",
        json={
            "email": email,
            "password": password,
        },
    )
    assert response.status_code == status_code


async def test_logout(ac: AsyncClient):
    response = await ac.post("auth/logout")
    assert response.status_code == 200


@pytest.mark.parametrize(
    "email,password,status_code",
    [
        ("user123@example.com", "string1234", 200),
    ],
)
async def test_delete(email, password, status_code, ac: AsyncClient):
    # Регистрация пользователя
    register_response = await ac.post(
        "auth/register",
        json={
            "email": email,
            "password": password,
        },
    )
    assert register_response.status_code == status_code

    # Получаем токен из ответа
    access_token = register_response.json()["access_token"]

    # Удаление пользователя с авторизацией
    response = await ac.delete(
        "auth/delete",
        headers={"Authorization": f"Bearer {access_token}"},
        cookies=register_response.cookies,
    )
    assert response.status_code == status_code

    # Проверяем что пользователь удален
    user = await UsersDAO.find_one_or_none(email=email)
    assert user is None
