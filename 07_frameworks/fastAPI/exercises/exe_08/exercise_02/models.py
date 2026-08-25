"""
See INSTRUCTIONS.md for the full task description.
"""

from sqlalchemy import Boolean, Column, Integer, String

from database import Base

# TODO: define the Task model
# __tablename__ = "tasks"
# columns: id (Integer, primary_key, index), title (String, nullable=False),
# done (Boolean, default=False)
class Tasks(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String,nullable=False)
    done = Column(Boolean, default=False)