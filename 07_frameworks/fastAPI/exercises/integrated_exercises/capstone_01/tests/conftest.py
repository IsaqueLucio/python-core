from fastapi.testclient import TestClient
import pytest
from app.models import User, UserRole, Project, Issue, IssuePriority, IssueStatus
from app.schemas import UserCreate, ProjectCreate, IssueCreate
from app.security import hash_password
from app.auth import create_access_token
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db
from app.main import app

@pytest.fixture
def test_db():
    TEST_DATABASE_URL = "sqlite:///./test.db"
    engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db    
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client(test_db):
    def override_get_db():
        yield test_db
    app.dependency_overrides[get_db] = override_get_db
    try:
        yield TestClient(app)
    finally:
        app.dependency_overrides.clear()

@pytest.fixture
def test_user(test_db):
    create_user  = UserCreate(
        username="Tester01",
        email="tester01@gmail.com",
        password="Password@123"
    )
    t_user = User(
        username = create_user.username,
        email = create_user.email,
        hashed_password = hash_password(create_user.password.get_secret_value()),
        role= UserRole.USER
    )
    test_db.add(t_user)
    test_db.commit()
    test_db.refresh(t_user)
    yield t_user

@pytest.fixture
def test_admin(test_db):
    create_admin = UserCreate(
        username="AdmTester01",
        email="Admtester@gmail.com",
        password="123@Password"
    )
    adm_user = User(
        username = create_admin.username,
        email = create_admin.email,
        hashed_password = hash_password(create_admin.password.get_secret_value()),
        role = UserRole.ADMIN
    )
    test_db.add(adm_user)
    test_db.commit()
    test_db.refresh(adm_user)
    yield adm_user

@pytest.fixture
def test_reporter(test_db):
    create_reporter_user = UserCreate(
        username="Reporter User",
        email="emailreporter@gmail.com",
        password="Senha@6657"
    )
    reporter = User(
        username = create_reporter_user.username,
        email = create_reporter_user.email,
        hashed_password = hash_password(create_reporter_user.password.get_secret_value()),
        role = UserRole.USER
    )
    test_db.add(reporter)
    test_db.commit()
    test_db.refresh(reporter)
    yield reporter

@pytest.fixture
def test_auth_user(test_user):
    token_data = {"sub": test_user.email}
    token = create_access_token(data=token_data)
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def test_auth_admin(test_admin):
    token_data = {"sub": test_admin.email}
    token = create_access_token(data=token_data)
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def test_auth_reporter(test_reporter):
    token_data = {"sub": test_reporter.email}
    token = create_access_token(data = token_data)
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def test_project(test_user, test_db):
    project_create = ProjectCreate(
        name="Project 01",
        description="Project 01 description."
    )
    project = Project(
        name = project_create.name,
        description = project_create.description,
        owner_id = test_user.id,
    )
    test_db.add(project)
    test_db.commit()
    test_db.refresh(project)
    yield project

@pytest.fixture
def test_issue(test_reporter, test_project, test_db):
    issue_create = IssueCreate(
        title="issue test",
        description="issue test description",
        status=IssueStatus.OPEN,
        priority=IssuePriority.MEDIUM
    )
    issue = Issue(
        title = issue_create.title,
        description = issue_create.description,
        status = issue_create.status,
        priority = issue_create.priority,
        project_id = test_project.id,
        reporter_id = test_reporter.id
    )
    test_db.add(issue)
    test_db.commit()
    test_db.refresh(issue)
    yield issue

