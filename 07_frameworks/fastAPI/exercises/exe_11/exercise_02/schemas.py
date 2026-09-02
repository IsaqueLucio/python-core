"""
See INSTRUCTIONS.md for the full task description.
"""

from pydantic import BaseModel, ConfigDict

# TODO: define ContactCreate (input model)
# fields: name (str), phone (str)
class ContactCreate(BaseModel):
    name: str
    phone: str

# TODO: define ContactOut (output model)
# fields: id (int), name (str), phone (str)
# remember model_config = ConfigDict(from_attributes=True)
class ContactOut(BaseModel):
    id: int
    name: str
    phone: str
    model_config = ConfigDict(from_attributes=True)