"""
See INSTRUCTIONS.md for the full task description.
"""

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


# TODO: define test_create_note()
# POST a note, assert status_code == 200, assert the response has
# the right "text"
def test_create_note():
    response = client.post("/notes",json={"text": "teste01"})
    assert response.status_code == 200
    data = response.json()
    assert data["text"] == "teste01"

# TODO: define test_get_all_notes()
# create one note, GET "/notes", assert status_code == 200, assert
# the created note is somewhere in the response list
def test_get_all_notes():
    client.post("/notes",json={"text": "teste02"})
    response = client.get("/notes")
    assert response.status_code == 200
    test_notes = [note["text"] for note in response.json()]
    assert "teste02" in test_notes

# TODO: define test_get_single_note_not_found()
# GET "/notes/999", assert status_code == 404
def test_get_single_note_not_found():
    response = client.get("/notes/999")
    assert response.status_code == 404
    post = client.post("/notes", json={"text": "teste03"})
    note_id = post.json()["id"]
    response2 = client.get(f"/notes/{note_id}")
    assert response2.status_code == 200
