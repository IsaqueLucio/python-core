"""
See INSTRUCTIONS.md for the full task description.
"""

from sqlalchemy import Column, Integer, String

from database import Base

# TODO: define the Account model
# __tablename__ = "accounts"
# columns: id (Integer, primary_key, index),
# email (String, unique=True, nullable=False),
# hashed_password (String, nullable=False),
# role (String, default="user")
class Account(Base):
    
    __tablename__="accounts"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="user")