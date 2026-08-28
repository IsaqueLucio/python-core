"""
All password-hashing and JWT logic lives here, isolated from the
endpoints in main.py -- the same "separate the reusable logic"
philosophy as dependencies.py in topic 7.
"""

from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt
from passlib.context import CryptContext

# In a REAL project, this key must come from an environment variable
# or a secrets manager -- NEVER hardcoded and NEVER committed to git.
# It's hardcoded here only because this is a learning example.
SECRET_KEY = "a-very-secret-key-change-this-in-real-projects"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# CryptContext handles hashing with bcrypt, plus safely comparing a
# plain password against a stored hash (never compare strings
# directly -- that's vulnerable to timing attacks).
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(plain_password: str) -> str:
    return pwd_context.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    """
    `data` is typically {"sub": username} -- "sub" (subject) is the
    JWT-standard field for "who this token is about".
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> str | None:
    """
    Returns the username stored in a valid token, or None if the
    token is invalid/expired/tampered with.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        return None
