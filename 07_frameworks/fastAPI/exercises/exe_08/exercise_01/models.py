"""
See INSTRUCTIONS.md for the full task description.
"""

from sqlalchemy import Column, Float, Integer, String

from database import Base

# TODO: define the Product model
# __tablename__ = "products"
# columns: id (Integer, primary_key, index), name (String, nullable=False),
# price (Float, nullable=False), quantity (Integer, default=0)
class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, default=0)

    