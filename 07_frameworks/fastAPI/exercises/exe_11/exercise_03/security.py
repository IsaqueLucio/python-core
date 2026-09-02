"""
Same password-hashing logic as topic 9 -- copy it.
"""

from passlib.context import CryptContext

# TODO: create the CryptContext (schemes=["bcrypt"], deprecated="auto")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# TODO: define hash_password(plain_password: str) -> str
def hash_password(plain_password: str) -> str:
    return pwd_context.hash(plain_password)

# TODO: define verify_password(plain_password: str, hashed_password: str) -> bool
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


