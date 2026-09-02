"""
See INSTRUCTIONS.md for the full task description. Same pattern as
topic 9's Account model.
"""

from sqlalchemy import Column, Integer, String

from database import Base

# TODO: define the Account model
# __tablename__ = "accounts"
# columns: id (Integer, primary_key, index),
# email (String, unique=True, nullable=False),
# hashed_password (String, nullable=False)
class Account(Base):
    __tablename__ = "accounts"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True,nullable=False)
    hashed_password = Column(String, nullable=False)