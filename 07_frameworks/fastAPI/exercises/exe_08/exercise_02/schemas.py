"""
See INSTRUCTIONS.md for the full task description.
"""

from pydantic import BaseModel, ConfigDict

# TODO: define TaskCreate (input model)
# fields: title (str), done (bool = False)
class TaskCreate(BaseModel):
    title: str
    done: bool = False

# TODO: define TaskUpdate (input model, for partial updates)
# fields: title (str | None = None), done (bool | None = None)
class TaskUpdate(BaseModel):
    title: str | None =None
    done: bool | None = None
# TODO: define TaskOut (output model)
# fields: id (int), title (str), done (bool)
# remember model_config = ConfigDict(from_attributes=True)
class TaskOut(BaseModel):
    id: int
    title: str
    done: bool
    model_config =  ConfigDict(from_attributes=True)