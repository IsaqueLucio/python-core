"""
Tests for main.py. Notice the file is named test_main.py -- pytest
automatically discovers any file matching test_*.py or *_test.py, and
inside it, any function starting with test_.
"""

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import Base, get_db
from main import app

# --- Setting up a SEPARATE, throwaway database just for tests ---
# This is a DIFFERENT SQLite file from app.db (the one main.py uses
# normally) -- so running tests never touches your real dev data.
TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    """
    Same shape as the real get_db() from database.py, but pointing at
    the test database instead. This function will be used INSTEAD OF
    get_db whenever a test triggers an endpoint.
    """
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# This is the key line: tell the app "whenever an endpoint asks for
# get_db, give it override_get_db instead". From this point on, EVERY
# request made through `client` uses the test database.
app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_create_item():
    response = client.post("/items", json={"name": "Keyboard"})

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Keyboard"
    # We don't assert an exact "id" value -- that depends on what
    # other tests ran before this one, and hardcoding it would make
    # this test fragile. Just check that it's the right TYPE.
    assert isinstance(data["id"], int)


def test_list_items_includes_created_item():
    # Create one first, so we know there's at least one to find.
    client.post("/items", json={"name": "Mouse"})

    response = client.get("/items")

    assert response.status_code == 200
    names = [item["name"] for item in response.json()]
    assert "Mouse" in names


def test_create_item_missing_name_fails_validation():
    # No "name" field at all -- Pydantic should reject this with 422,
    # the exact same automatic validation from topic 4.
    response = client.post("/items", json={})

    assert response.status_code == 422
    
