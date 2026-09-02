"""
See INSTRUCTIONS.md for the full task description.

Follow the exact pattern from theory/11_testing/test_main.py.
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

# TODO: define test_create_contact()
def test_create_contact():
    response = client.post("/contacts", json={"name": "teste01", "phone": "123"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "teste01"
    assert data["phone"] == "123"
    assert isinstance(data["id"], int)

# TODO: define test_get_contact_by_id()
def test_get_contact_by_id():
    post = client.post("/contacts", json={"name": "teste02", "phone": "456"})
    data = post.json()
    response = client.get(f"/contacts/{data['id']}")
    assert response.status_code == 200

# TODO: define test_list_contacts()
def test_list_contacts():
    client.post("/contacts", json={"name": "teste03", "phone": "789"})
    response = client.get("/contacts")
    assert response.status_code == 200
    data = response.json()
    names = [item["name"] for item in data]
    phones = [item["phone"] for item in data]
    assert "teste03" in names
    assert "789" in phones
    assert isinstance(data[0]["id"], int)

# TODO: define test_delete_contact()
# create one, capture its id, delete it, assert 200, then GET again
# and assert that id is no longer in the list
def test_delete_contact():
    post = client.post("/contacts", json={"name": "teste04", "phone": "101112"})
    contact_id = post.json()["id"]
    response = client.get("/contacts")
    data = response.json()
    response2 = client.delete(f"/contacts/{contact_id}")
    assert response2.status_code == 200
    response3 = client.get(f"/contacts/{contact_id}")
    assert response3.status_code == 404

# TODO: define test_delete_nonexistent_contact_returns_404()
def test_delete_nonexistent_contact_returns_404():
    response = client.delete("/contacts/999")
    assert response.status_code == 404

