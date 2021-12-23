from functools import lru_cache

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    auth_cookie_name: str
    salt: str
    db_url: str = Field(..., env="DATABASE_URL")

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()
