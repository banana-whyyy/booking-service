from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    database_url: str = Field(
        default="postgresql+asyncpg://postgres:postgres@db:5432/Booking_DB",
        validation_alias="DATABASE_URL",
    )
    sync_database_url: str = Field(
        default="postgresql+psycopg://postgres:postgres@db:5432/Booking_DB",
        validation_alias="SYNC_DATABASE_URL",
    )

    redis_url: str = Field(
        default="redis://:redis_password@redis:6379/0",
        validation_alias="REDIS_URL",
    )

    secret_key: str = Field(..., validation_alias="SECRET_KEY")
    algorithm: str = Field(default="HS256", validation_alias="ALGORITHM")
    access_token_expire_minutes: int = Field(
        default=30, validation_alias="ACCESS_TOKEN_EXPIRE_MINUTES"
    )
    refresh_token_expire_days: int = Field(
        default=30, validation_alias="REFRESH_TOKEN_EXPIRE_DAYS"
    )
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False, 
    )

settings = Settings()