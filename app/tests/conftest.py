import asyncio
import json
import httpx
import motor
from motor.motor_asyncio import AsyncIOMotorClient
import pytest
from sqlalchemy import insert
from app.database import Base, async_session_maker, engine
from app.config import settings
from app.main import app as fast_apiapp
from app.users.models import Users
from httpx import AsyncClient


@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    assert settings.MODE == "TEST"

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    def open_mock_json(model: str):
        with open(f"app/tests/mock_{model}.json", "r") as file:
            return json.load(file)

    users = open_mock_json("users")

    async with async_session_maker() as session:
        add_users = insert(Users).values(users)

        await session.execute(add_users)
        await session.commit()


@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def ac():
    async with AsyncClient(
        transport=httpx.ASGITransport(app=fast_apiapp),
        base_url="http://test",
        follow_redirects=True,
    ) as ac:
        yield ac


@pytest.fixture(scope="function")
async def session():
    async with async_session_maker() as session:
        yield session


@pytest.fixture(scope="function")
async def mongodb():
    client = AsyncIOMotorClient(
        settings.TEST_MONGODB_URL,
        maxPoolSize=100,
        minPoolSize=10,
    )
    mongodb = client[settings.MONGO_INITDB_DB_NAME]
    yield mongodb
    await client.drop_database(settings.MONGO_INITDB_DB_NAME)
    client.close()
