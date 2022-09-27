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
    ENVIRONMENT: str
    API_TOKEN: Secret
    SECRET_KEY: Secret
    POSTGRES_SERVER: str = Field(..., env="POSTGRES_URL")
    POSTGRES_USER: str = Field(..., env="POSTGRES_USER")
    POSTGRES_PASSWORD: str = Field(..., env="POSTGRES_PASSWORD")
    POSTGRES_DB: str = Field(..., env="POSTGRES_DATABASE")
    POSTGRES_PORT: str = Field(..., env="POSTGRES_PORT")
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    API_V1_ENDPOINT: str = "/api/v1"
    MANAGEMENT_APP_NAME: str = "management"
    MANAGEMENT_UUID: str = os.getenv("MANAGEMENT_UUID", str(uuid4()))

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql+psycopg2",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER", "127.0.0.1"),
            port=values.get("POSTGRES_PORT", 5432),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )


class DevSettings(Settings):
    DEBUG: bool = True
    ENVIRONMENT: str = "development"
    API_TOKEN: Secret = Fernet.generate_key()
    SECRET_KEY: Secret = Field(..., env="FIGURE_HOOK_SECRET")

    class Config:
        env_file = "dev.env"
        env_file_encoding = "utf-8"


class TestSettings(Settings):
    DEBUG: bool = True
    ENVIRONMENT: str = "test"
    API_TOKEN: Secret = Fernet.generate_key()
    SECRET_KEY: Secret = Fernet.generate_key()

    class Config:
        env_file = "test.env"
        env_file_encoding = "utf-8"


class ProductionSettings(Settings):
    API_TOKEN: Secret = Field(..., env="API_TOKEN")
    SECRET_KEY: Secret = Field(..., env="FIGURE_HOOK_SECRET")
    ENVIRONMENT: str = "production"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


def get_settings() -> Settings:
    env = os.getenv("ENV")
    if env == "development":
        return DevSettings()  # type: ignore
    if env == "production":
        return ProductionSettings()  # type: ignore
    if env == "test":
        return TestSettings()  # type: ignore

    return DevSettings()  # type: ignore


settings = get_settings()
