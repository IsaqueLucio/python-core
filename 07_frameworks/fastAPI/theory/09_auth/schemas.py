"""
Pydantic schemas. Notice UserOut has NO password field at all --
same "never leak sensitive fields" principle from topic 5.
"""

from pydantic import BaseModel, ConfigDict


class UserCreate(BaseModel):
    username: str
    password: str  # plain password, only ever used as INPUT


class UserOut(BaseModel):
    id: int
    username: str
    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
