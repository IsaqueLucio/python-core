"""
Centralizes configuration, read from environment variables (via a
.env file locally, or real environment variables in production/Docker
-- pydantic-settings handles both the same way).
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    class Config:
        env_file = ".env"


# Created once, imported everywhere else that needs configuration --
# same "single source of truth" idea as database.py's engine/Base.
settings = Settings()
