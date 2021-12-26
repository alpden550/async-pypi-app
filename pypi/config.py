from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    auth_cookie_name: str
    salt: str
    database_url: str
    async_database_url: str

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()
