from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from app.config import settings

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return token

def decode_access_token(token: str) -> str | None:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=settings.algorithm)
        return payload.get("sub")
    except JWTError:
        return None
