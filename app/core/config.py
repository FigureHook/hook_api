import os
from typing import Any, Dict, Optional, Union
from uuid import uuid4

from cryptography.fernet import Fernet
from dotenv import load_dotenv
from pydantic import BaseSettings, Field, PostgresDsn, validator

load_dotenv()

Secret = Union[str, bytes]


class Settings(BaseSettings):
    DEBUG: bool = False
    API_TOKEN: Secret = os.getenv('API_TOKEN', Fernet.generate_key())
    ENVIRONMENT: str
    SECRET_KEY: Secret = Fernet.generate_key()
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    API_V1_ENDPOINT: str = "/api/v1"
    MANAGEMENT_APP_NAME: str = 'management'
    MANAGEMENT_UUID: str = os.getenv('MANAGEMENT_UUID', str(uuid4()))

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
    DEBUG: bool = True
    SECRET_KEY: Secret = Fernet.generate_key()
    POSTGRES_SERVER: str = 'db'
    POSTGRES_USER: str = 'kappa'
    POSTGRES_PASSWORD: str = 'test'
    POSTGRES_DB: str = 'hook_api'


class TestSettings(DevSettings):
    ENVIRONMENT: str = 'test'
    POSTGRES_DB: str = 'hook_api_test'


class ProductionSettings(Settings):
    SECRET_KEY: Secret = Field(..., env='SECRET_KEY')
    POSTGRES_SERVER: str = Field(..., env='POSTGRES_URL')
    POSTGRES_USER: str = Field(..., env='POSTGRES_USER')
    POSTGRES_PASSWORD: str = Field(..., env='POSTGRES_PASSWORD')
    POSTGRES_DB: str = Field(..., env='POSTGRES_DATABASE')

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


def get_settings() -> Settings:
    env = os.getenv('ENV')
    if env == 'development':
        return DevSettings(ENVIRONMENT=env)
    if env == 'production':
        return ProductionSettings(ENVIRONMENT=env)  # type: ignore
    if env == 'test':
        return TestSettings(ENVIRONMENT=env)

    return DevSettings(ENVIRONMENT='development')


settings = get_settings()
