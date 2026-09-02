# Exercise 1: Basic tests (no database)

## Goal
Practice the core TestClient + assert pattern on a simple app, without
the added complexity of dependency_overrides yet -- that comes in
exercise 2.

## Structure to build

    exercise_01/
    ├── main.py
    └── test_main.py

## Instructions

1. In `main.py`, build a small in-memory (list-based, like topics
   1-6 -- no database needed here) "notes" API:
   - a module-level list `notes = []`
   - `POST "/notes"` with a required body field `text: str` (use a
     Pydantic model `NoteCreate`): appends `{"id": len(notes) + 1,
     "text": text}` to `notes`, returns it
   - `GET "/notes"`: returns the full `notes` list
   - `GET "/notes/{note_id}"`: returns the matching note, or
     `raise HTTPException(404, "Note not found")`

2. In `test_main.py`:
   - `from fastapi.testclient import TestClient`
   - `from main import app`
   - `client = TestClient(app)`
   - `def test_create_note():` -- POST a note, assert status_code == 200,
     assert the response JSON has the right "text"
   - `def test_get_all_notes():` -- create one note, then GET "/notes",
     assert status_code == 200, assert the note you created is
     somewhere in the response list
   - `def test_get_single_note_not_found():` -- GET "/notes/999" (an
     id that surely doesn't exist), assert status_code == 404

## Run it

From INSIDE the `exercise_01/` folder:

    pytest -v

All 3 tests should show PASSED. If any fails, pytest shows you
exactly which assertion didn't match -- read that output carefully,
it tells you what it expected vs what it actually got.
