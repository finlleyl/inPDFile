import pytest
from app.users.dao import UsersDAO


@pytest.mark.parametrize(
    "user_id, email, exists",
    [
        (1, "user@example.com", True),
        (2, "user1@example.com", True),
        (1000, "None", False),
    ],
)
async def test_find_one_or_none(user_id, email, exists):
    """
    Тестирование метода find_one_or_none класса UsersDAO.

    Проверяет, что метод возвращает пользователя с указанным id, если он существует.
    Если пользователя с указанным id не существует, метод должен вернуть None.

    Параметры:
    id (int): id пользователя
    email (str): email пользователя
    exists (bool): флаг, указывающий, существует ли пользователь с указанным id
    """
    user = await UsersDAO.find_one_or_none(id=user_id)
    if exists:
        assert user
        assert user.email == email
        assert user.id == user_id
    else:
        assert not user


# async def test_find_all():
#     """
#     Тестирование метода find_all класса UsersDAO.

#     Проверяет, что метод возвращает всех активных пользователей, всех суперпользователей и всех пользователей.

#     Проверяет, что количество активных пользователей равно 3, количество суперпользователей равно 1, а общее количество пользователей равно 3.
#     """
#     active_users = await UsersDAO.find_all(is_active=True)
#     super_users = await UsersDAO.find_all(is_superuser=True)
#     all_users = await UsersDAO.find_all()

#     assert len(active_users) == 3
#     assert len(super_users) == 1
#     assert len(all_users) == 3


async def test_add():
    """
    Тестирование методов add и find_one_or_none класса UsersDAO.

    Создает тестовые данные для нового пользователя и добавляет его в базу данных с помощью метода add.
    Проверяет, что возвращаемый id не равен None.
    Затем находит пользователя по id с помощью метода find_one_or_none и проверяет, что все поля пользователя соответствуют ожидаемым значениям.
    """
    new_user_data = {
        "email": "test@example.com",
        "hashed_password": "hashedpass123",
        "is_superuser": True,
    }

    user_id = await UsersDAO.add(**new_user_data)
    assert user_id is not None

    user = await UsersDAO.find_one_or_none(id=user_id)
    assert user is not None and all(
        [
            user.is_verified is False,
            user.is_active is True,
            user.is_superuser is True,
            user.registration_date is not None,
            user.last_login_date is not None,
            user.email == new_user_data["email"],
        ]
    )


async def test_delete():
    """
    Тестирование метода delete класса UsersDAO.

    Проверяет, что метод удаляет пользователя с указанным email.

    Проверяет, что количество пользователей после удаления на 1 меньше, чем количество пользователей до удаления.
    """
    user_count = len(await UsersDAO.find_all())
    await UsersDAO.delete(email="test@example.com")
    new_user_count = len(await UsersDAO.find_all())
    assert new_user_count == user_count - 1
