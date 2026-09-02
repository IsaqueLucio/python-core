"""
See INSTRUCTIONS.md for the full task description.
"""

from sqlalchemy import Column, Integer, String

from database import Base

# TODO: define the Book model
# __tablename__ = "books"
# columns: id (Integer, primary_key, index), title (String, nullable=False),
# author (String, nullable=False)
class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    