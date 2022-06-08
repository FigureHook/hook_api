import os
from typing import Any, Dict, Optional, Union

from cryptography.fernet import Fernet
from pydantic import BaseSettings, PostgresDsn, validator

Secret = Union[str, bytes]


class Settings(BaseSettings):
    SECRET_KEY: Secret = Fernet.generate_key()
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    API_V1_ENDPOINT: str = "/api/v1"

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql+psycopg2",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER", '127.0.0.1'),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )


class DevSettings(Settings):
    SECRET_KEY: Secret = Fernet.generate_key()
    POSTGRES_SERVER: str = 'db'
    POSTGRES_USER: str = 'kappa'
    POSTGRES_PASSWORD: str = 'test'
    POSTGRES_DB: str = 'hook_api'


class TestSettings(DevSettings):
    POSTGRES_DB: str = 'hook_api_test'


class ProductionSettings(Settings):
    SECRET_KEY: Secret = os.getenv("SECRET_KEY", Fernet.generate_key())
    POSTGRES_SERVER: str = os.getenv("POSTGRES_URL", 'db')
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", 'postgres')
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", 'password')
    POSTGRES_DB: str = os.getenv("POSTGRES_DATABASE", 'hook_api')


def get_settings() -> Settings:
    env = os.getenv('ENV')
    if env == 'development':
        return DevSettings()
    if env == 'production':
        return ProductionSettings()
    if env == 'test':
        return TestSettings()

    return DevSettings()


settings = get_settings()
