"""
See INSTRUCTIONS.md for the full task description.
"""

from pydantic import BaseModel, ConfigDict

# TODO: define AuthorCreate (input model)
# fields: name (str), country (str)
class AuthorCreate(BaseModel):
    name: str
    country: str

# TODO: define BookCreate (input model)
# fields: title (str), author_id (int)
class BookCreate(BaseModel):
    title: str
    author_id: int

# TODO: define BookOut (output model)
# fields: id (int), title (str), author_id (int)
# remember model_config = ConfigDict(from_attributes=True)
class BookOut(BaseModel):
    id: int
    title: str
    author_id: int
    model_config = ConfigDict(from_attributes=True)

# TODO: define AuthorOut (output model)
# fields: id (int), name (str), country (str), books (list[BookOut] = [])
# remember model_config = ConfigDict(from_attributes=True)
# NOTE: AuthorOut must be defined AFTER BookOut, since it references it
class AuthorOut(BaseModel):
    id: int
    name: str
    country: str
    books: list[BookOut] = []
    model_config = ConfigDict(from_attributes=True)
