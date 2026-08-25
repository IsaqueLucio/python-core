"""
SQLAlchemy ORM models -- these map directly to database tables.
Compare each of these to a JPA @Entity class: same idea, different
syntax.
"""

from sqlalchemy import Boolean, Column, Integer, String

from database import Base


class Book(Base):
    __tablename__ = "books"

    # Column(..., primary_key=True) is the equivalent of @Id.
    # index=True speeds up lookups by this column (like a JPA @Index).
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    available = Column(Boolean, default=True)
