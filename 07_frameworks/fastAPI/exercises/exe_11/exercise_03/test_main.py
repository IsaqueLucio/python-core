"""
See INSTRUCTIONS.md for the full task description.
"""

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import Base, get_db
from main import app

# TODO: set up a separate test database (sqlite:///./test.db)
# create engine, TestingSessionLocal, and Base.metadata.create_all
TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

# TODO: define override_get_db() -- same shape as the real get_db,
# but using TestingSessionLocal
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# TODO: app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_db] = override_get_db

# TODO: client = TestClient(app)
client = TestClient(app)

# TODO: define test_register_new_account()
# assert 200, assert no "password" field in the response
def test_register_new_account():
    response = client.post("/register", json={"email": "teste01@email.com", "password": "teste123"})
    assert response.status_code == 200
    data = response.json()
    assert "password" not in data

# TODO: define test_register_duplicate_email_fails()
# register the same email twice, assert the SECOND attempt is 409
def test_register_duplicate_email_fails():
    response = client.post("/register", json={"email": "teste02@email.com", "password": "teste321"})
    response2 = client.post("/register", json={"email": "teste02@email.com", "password": "test_email"})
    assert response2.status_code == 409

# TODO: define test_login_with_correct_credentials()
# register a NEW account (unique email!), then log in with
# client.post("/login", data={"username": email, "password": password})
# assert 200, assert "access_token" is in the response
def test_login_with_correct_credentials():
    client.post("/register", json={"email": "teste03@email.com", "password": "teste456"})
    response = client.post("/login", data={"username": "teste03@email.com", "password": "teste456"})
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data

# TODO: define test_login_with_wrong_password_fails()
# register, then try logging in with the wrong password, assert 401
def test_login_with_wrong_password_fails():
    client.post("/register", json={"email": "teste04@email.com", "password": "teste654"})
    response = client.post("/login", data={"username": "teste04@email.com", "password": "00000"})
    assert response.status_code == 401

# TODO: define test_protected_endpoint_without_token_fails()
# GET "/me" with no Authorization header, assert 401
def test_protected_endpoint_without_token_fails():
    response = client.get("/me")
    assert response.status_code == 401

# TODO: define test_protected_endpoint_with_valid_token_succeeds()
# register + login to get a real token, then GET "/me" with
# headers={"Authorization": f"Bearer {token}"}, assert 200, assert
# the email matches
def test_protected_endpoint_with_valid_token_succeeds():
    register = client.post("/register", json={"email": "teste05@email.com", "password": "teste789"})
    login = client.post("/login", data={"username": "teste05@email.com", "password": "teste789"})
    data = login.json()
    get_me = client.get("/me", headers={"Authorization": f"Bearer {data["access_token"]}"})
    assert get_me.status_code == 200

