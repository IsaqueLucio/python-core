"""
See INSTRUCTIONS.md for the full task description.
"""

from sqlalchemy import Column, Integer, String

from database import Base

# TODO: define the Contact model
# __tablename__ = "contacts"
# columns: id (Integer, primary_key, index), name (String, nullable=False),
# phone (String, nullable=False)
class Contact(Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    phone = Column(String, nullable=False)