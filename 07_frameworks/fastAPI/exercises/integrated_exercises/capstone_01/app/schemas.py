from pydantic import BaseModel, ConfigDict, EmailStr, SecretStr, Field, field_validator
from app.models import UserRole, IssueStatus, IssuePriority
from typing import Optional

#Users ==================================================
class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50, description="Username, between 3 and 50 characters.")
    email: EmailStr = Field(description="Valid email.")
    password: SecretStr = Field(min_length=8, description='''
    -Must contain at least one uppercase letter.\n
    -Must contain at least 1 number.\n
    -Must contain at least 1 special character.
    ''')
    @field_validator("password")
    @classmethod
    def password_complexity(cls, v: SecretStr) -> SecretStr:
        pwd = v.get_secret_value()
        if not any(c.isupper() for c in pwd):
            raise ValueError("Must contain at least one uppercase letter.")
        if not any(c.isdigit() for c in pwd):
            raise ValueError("Must contain at least 1 number.")
        if not any(c in "!@#$%^&*()_+-=" for c in pwd):
            raise ValueError("Must contain at least 1 special character.")
        return v

class UserOut(BaseModel):
    id: int
    username: str
    email: str
    role: UserRole
    model_config = ConfigDict(from_attributes=True)

#Projects ===============================================
class ProjectCreate(BaseModel):
    name: str = Field(min_length=1, max_length=50, description="Project name.")
    description: Optional[str] = None

class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class ProjectOut(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    owner_id: int
    model_config = ConfigDict(from_attributes=True)

#Issues =================================================
class IssueCreate(BaseModel):
    title: str = Field(min_length=1, max_length=50, description="Issue name.")
    description: Optional[str] = None
    status: IssueStatus
    priority: IssuePriority

class IssueUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[IssueStatus] = None
    priority: Optional[IssuePriority] = None

class IssueOut(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    status: IssueStatus
    priority: IssuePriority
    project_id: int
    reporter_id: int
    model_config = ConfigDict(from_attributes=True)

#Token =================================================
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

#GitHubProfileOut ======================================
class GitHubProfileOut(BaseModel):
    login: str
    name: Optional[str] = None
    public_repos: int
    html_url: str
    model_config = ConfigDict(from_attributes=True)
