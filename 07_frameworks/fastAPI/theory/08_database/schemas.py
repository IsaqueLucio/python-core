"""
Pydantic schemas -- these describe the API's input/output shape, NOT
the database table directly (that's models.py). This is the same
Input/Output model separation from topic 5 (response_model), applied
on top of a real database now instead of a plain dict.
"""

from pydantic import BaseModel, ConfigDict


class BookCreate(BaseModel):
    title: str
    author: str
    available: bool = True


class BookOut(BaseModel):
    id: int
    title: str
    author: str
    available: bool

    # This tells Pydantic it's allowed to read data from an ORM
    # object's ATTRIBUTES (book.title), not just from a dict
    # (book["title"]) -- required whenever a response_model wraps a
    # SQLAlchemy object instead of a plain dict.
    model_config = ConfigDict(from_attributes=True)
