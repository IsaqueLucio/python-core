"""
See INSTRUCTIONS.md for the full task description.
"""

from pydantic_settings import BaseSettings

# TODO: define the Settings class
# fields: secret_key (str, required), algorithm (str, default "HS256"),
# access_token_expire_minutes (int, default 30)
# don't forget: class Config: env_file = ".env"
class Settings(BaseSettings):
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    class Config:
        env_file = ".env"

# TODO: create settings = Settings() at module level
settings = Settings()