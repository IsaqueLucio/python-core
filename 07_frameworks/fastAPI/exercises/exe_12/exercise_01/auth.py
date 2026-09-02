"""
See INSTRUCTIONS.md for the full task description.

Same JWT logic as topic 9, but now reading configuration from
Settings instead of hardcoded constants.
"""

from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt

# TODO: import settings from config
from config import settings

# TODO: define create_access_token(data: dict) -> str
# use settings.secret_key, settings.algorithm,
# settings.access_token_expire_minutes instead of hardcoded constants
def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return token

# TODO: define decode_access_token(token: str) -> str | None
# use settings.secret_key and settings.algorithm
def decode_access_token(token: str) -> str | None:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=settings.algorithm)
        return payload.get("sub")
    except JWTError:
        return None
    