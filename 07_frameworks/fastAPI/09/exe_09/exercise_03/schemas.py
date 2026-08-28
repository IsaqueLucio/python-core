"""
See INSTRUCTIONS.md for the full task description.
"""

from pydantic import BaseModel, ConfigDict

# TODO: define AccountCreate (input model)
# fields: email (str), password (str)
class AccountCreate(BaseModel):
    email: str
    password: str

# TODO: define AccountOut (output model)
# fields: id (int), email (str), role (str) -- no password!
# remember model_config = ConfigDict(from_attributes=True)
class AccountOut(BaseModel):
    id: int
    email: str
    role: str
    model_config = ConfigDict(from_attributes=True)

# TODO: define Token (output model)
# fields: access_token (str), token_type (str = "bearer")
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

    