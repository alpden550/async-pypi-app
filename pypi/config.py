from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    auth_cookie_name: str
    salt: str

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()
