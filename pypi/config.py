from pydantic import BaseSettings


class Settings(BaseSettings):
    auth_cookie_name: str

    class Config:
        env_file = ".env"


settings = Settings()
