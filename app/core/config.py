from pathlib import Path
from typing import Any, List, Optional, Union

from dotenv import load_dotenv
from pydantic import PostgresDsn, field_validator
from pydantic_core.core_schema import ValidationInfo
from pydantic_settings import BaseSettings

load_dotenv('.env')
BASE_DIR = Path(__file__).resolve().parent


class Settings(BaseSettings):
    """SERVER CONFIG"""
    DEBUG: bool | None = None

    # API
    COINMARKETCAP_API_KEY: str
    # WALLET
    PRIZM_WALLET_ADDRESS: str
    PRIZM_WALLET_SECRET_ADDRESS: str
    PRIZM_API_URL: str

    PRIZM_WALLET_ADDRESS_PAYOUT: str
    PRIZM_WALLET_ADDRESS_PARTNER_COMMISSION: str

    BOT_TOKEN: str
    CHANNEL_TO_CHECK: str

    @field_validator("DEBUG", mode="before")
    def assemble_debug(cls, v: Union[str, List[str]], values: ValidationInfo) -> Any:
        if v:
            return v
        else:
            return False

    """DATABASE CONFIG"""
    POSTGRES_HOST: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_PORT: str
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    ALEMBIC_DATABASE_URI: Optional[str] = None

    @field_validator("SQLALCHEMY_DATABASE_URI", mode='before')
    def assemble_db_connection(cls, v: Optional[str], values: ValidationInfo) -> Any:
        if isinstance(v, str):
            return v
        user = values.data.get("POSTGRES_USER")
        password = values.data.get("POSTGRES_PASSWORD")
        host = values.data.get("POSTGRES_HOST")
        db = values.data.get("POSTGRES_DB")
        port = values.data.get("POSTGRES_PORT")

        if all([user, password, host, db]):
            return f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{db}"
        else:
            return None

    @field_validator("ALEMBIC_DATABASE_URI", mode='before')
    def assemble_alembic_db_connection(cls, v: Optional[str], values: ValidationInfo) -> Any:
        if isinstance(v, str):
            return v
        user = values.data.get("POSTGRES_USER")
        password = values.data.get("POSTGRES_PASSWORD")
        host = values.data.get("POSTGRES_HOST")
        db = values.data.get("POSTGRES_DB")
        port = values.data.get("POSTGRES_PORT")

        if all([user, password, host, db]):
            return f"postgresql://{user}:{password}@{host}:{port}/{db}"
        else:
            return None

    """REDIS CONFIG"""
    REDIS_HOST: str
    REDIS_PASSWORD: str
    REDIS_PORT: int
    REDIS_DEFAULT_DB: str

    class Config:
        case_sensitive = True


settings = Settings()
