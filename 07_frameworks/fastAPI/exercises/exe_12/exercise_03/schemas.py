"""
See INSTRUCTIONS.md for the full task description.
"""

from pydantic import BaseModel, ConfigDict

# TODO: define BookCreate (input model)
# fields: title (str), author (str)
class BookCreate(BaseModel):
    title: str
    author: str

# TODO: define BookOut (output model)
# fields: id (int), title (str), author (str)
# remember model_config = ConfigDict(from_attributes=True)
class BookOut(BaseModel):
    id: int
    title: str
    author: str
    model_config = ConfigDict(from_attributes=True)

    