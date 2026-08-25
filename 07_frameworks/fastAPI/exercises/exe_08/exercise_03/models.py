"""
See INSTRUCTIONS.md for the full task description.
"""

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base

# TODO: define the Author model
# __tablename__ = "authors"
# columns: id (Integer, primary_key, index), name (String, nullable=False),
# country (String, nullable=False)
# relationship: books = relationship("Book", back_populates="author")
class Author(Base):
    __tablename__ = "authors"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    country = Column(String, nullable=False)
    books = relationship("Book", back_populates = "author")

# TODO: define the Book model
# __tablename__ = "books"
# columns: id (Integer, primary_key, index), title (String, nullable=False),
# author_id = Column(Integer, ForeignKey("authors.id"))
# relationship: author = relationship("Author", back_populates="books")
class Book(Base):
    __tablename__="books"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    author_id = Column(Integer, ForeignKey("authors.id"))
    author = relationship("Author", back_populates="books")