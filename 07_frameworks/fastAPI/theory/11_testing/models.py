"""
A simple Item model -- kept intentionally minimal so the tests below
stay focused on TESTING patterns, not on a complex domain.
"""

from sqlalchemy import Column, Integer, String

from database import Base


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
