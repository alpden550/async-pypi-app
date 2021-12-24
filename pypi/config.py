from functools import lru_cache

from pydantic import BaseSettings, PostgresDsn


class Settings(BaseSettings):
    auth_cookie_name: str
    salt: str
    database_url: PostgresDsn

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()
