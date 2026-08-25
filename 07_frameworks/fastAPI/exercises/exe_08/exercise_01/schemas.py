"""
See INSTRUCTIONS.md for the full task description.
"""

from pydantic import BaseModel, ConfigDict

# TODO: define ProductCreate (input model)
# fields: name (str), price (float), quantity (int = 0)
class ProductCreate(BaseModel):
    name: str
    price: float
    quantity: int = 0

# TODO: define ProductOut (output model)
# fields: id (int), name (str), price (float), quantity (int)
# remember model_config = ConfigDict(from_attributes=True)
class ProductOut(BaseModel):
    id: int
    name: str
    price: float
    quantity: int
    model_config = ConfigDict(from_attributes=True)

