"""
See INSTRUCTIONS.md for the full task description.

JWT creation/verification. Separate from security.py on purpose --
security.py handles PASSWORDS, auth.py handles TOKENS. Two different
responsibilities, two different files.
"""

from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt

# TODO: define SECRET_KEY, ALGORITHM ("HS256"),
# ACCESS_TOKEN_EXPIRE_MINUTES (30) as module-level constants
SECRET_KEY = "a-very-secret-key-change-this-in-real-projects"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# TODO: define create_access_token(data: dict) -> str
# copy the pattern from theory/09_auth/auth.py
def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# TODO: define decode_access_token(token: str) -> str | None
# copy the pattern from theory/09_auth/auth.py
def decode_access_token(token: str) -> str | None:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        return None
