from typing import ClassVar, Literal

from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    MODE: Literal["DEV", "PROD", "TEST"]
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    TEST_DB_HOST: str
    TEST_DB_PORT: int
    TEST_DB_USER: str
    TEST_DB_PASS: str
    TEST_DB_NAME: str

    TEST_MONGO_INITDB_DB_HOST: str

    REDIS_HOST: str
    REDIS_PORT: int

    MONGO_INITDB_DB_HOST: str
    MONGO_INITDB_DB_PORT: int
    MONGO_INITDB_ROOT_USERNAME: str
    MONGO_INITDB_DB_NAME: str
    MONGO_INITDB_ROOT_PASSWORD: str

    @property
    def DATABASE_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def TEST_DATABASE_URL(self):
        return f"postgresql+asyncpg://{self.TEST_DB_USER}:{self.TEST_DB_PASS}@{self.TEST_DB_HOST}:{self.TEST_DB_PORT}/{self.TEST_DB_NAME}"

    @property
    def MONGODB_URL(self):
        return f"mongodb://{self.MONGO_INITDB_ROOT_USERNAME}:{self.MONGO_INITDB_ROOT_PASSWORD}@{self.MONGO_INITDB_DB_HOST}:{self.MONGO_INITDB_DB_PORT}/?authSource={self.MONGO_INITDB_ROOT_USERNAME}"

    @property
    def TEST_MONGODB_URL(self):
        return f"mongodb://{self.MONGO_INITDB_ROOT_USERNAME}:{self.MONGO_INITDB_ROOT_PASSWORD}@{self.TEST_MONGO_INITDB_DB_HOST}:{self.MONGO_INITDB_DB_PORT}/?authSource={self.MONGO_INITDB_ROOT_USERNAME}"

    SECRET_KEY: str
    ALGORITHM: str

    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    LOG_LEVEL: Literal["DEBUG", "INFO", "WARN", "ERROR", "FATAL"]

    model_config = ConfigDict(env_file=".env")


settings = Settings()
