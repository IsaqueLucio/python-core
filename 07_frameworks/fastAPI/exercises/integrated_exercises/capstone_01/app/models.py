from sqlalchemy import Column, Integer, String, ForeignKey
from enum import Enum as PyEnum
from sqlalchemy.orm import relationship
from app.database import Base

class UserRole(str, PyEnum):
    USER = "user"
    ADMIN = "admin"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, nullable=False, default=UserRole.USER)
    
    projects = relationship("Project", back_populates="user")
    reported_issues = relationship("Issue", back_populates="reporter")

class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    owner_id = Column(ForeignKey("users.id"), nullable=False)
    
    user = relationship("User", back_populates="projects")
    issues = relationship("Issue", back_populates="project", cascade="all, delete-orphan")

class IssueStatus(str, PyEnum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    CLOSED = "closed"

class IssuePriority(str, PyEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class Issue(Base):
    __tablename__ = "issues"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    status = Column(String, nullable=False, default=IssueStatus.OPEN)
    priority = Column(String, nullable=False, default=IssuePriority.MEDIUM)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    reporter_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    project = relationship("Project", back_populates="issues")
    reporter = relationship("User", back_populates="reported_issues")