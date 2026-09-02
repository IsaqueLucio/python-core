# Exercise 2: Testing with a database (dependency_overrides)

## Goal
Practice the single most important FastAPI testing pattern: swapping
the real database for a throwaway test database, using
app.dependency_overrides.

## Structure to build

    exercise_02/
    ├── database.py    (same generic file from topic 8, copy it)
    ├── models.py
    ├── schemas.py
    ├── main.py
    └── test_main.py

## Instructions

1. `database.py`: copy the generic version (same as every exercise
   since topic 8).

2. In `models.py`:
   - Define `class Contact(Base):` with `__tablename__ = "contacts"`
   - Columns: id (Integer, primary_key, index), name (String,
     nullable=False), phone (String, nullable=False)

3. In `schemas.py`:
   - `ContactCreate` (input): name (str), phone (str)
   - `ContactOut` (output): id (int), name (str), phone (str), with
     `model_config = ConfigDict(from_attributes=True)`

4. In `main.py`:
   - `Base.metadata.create_all(bind=engine)` + create the app
   - `POST "/contacts"` (response_model=ContactOut): create a contact
   - `GET "/contacts"` (response_model=list[ContactOut]): list all
   - `GET "/contacts/{contact_id}"` (response_model=ContactOut): find 
     by id, raise HTTPException(404, "Contact not found") if missing
   - `DELETE "/contacts/{contact_id}"`: find by id, raise
     HTTPException(404, "Contact not found") if missing, otherwise
     delete it and return {"message": "Contact deleted"}

5. In `test_main.py` (follow the EXACT pattern from
   theory/11_testing/test_main.py):
   - set up a SEPARATE test database connection
     (`sqlite:///./test.db`, a different file from `app.db`)
   - define `override_get_db()` yielding a session from that test
     engine
   - `app.dependency_overrides[get_db] = override_get_db`
   - `client = TestClient(app)`
   - `def test_create_contact():` -- POST a contact, assert
     status_code == 200, assert the name/phone match
   - `def test_list_contacts():` -- create one, then GET, assert it
     appears in the list
   - `def test_get_contact_by_id():` -- create one, note its "id", 
     GET "/contacts/{id}", assert status_code == 200 and data matches
   - `def test_get_nonexistent_contact_returns_404():` -- GET 
     "/contacts/999999", assert status_code == 404
   - `def test_delete_contact():` -- create one, note its "id" from
     the response, DELETE it, assert status_code == 200, THEN also
     GET "/contacts/{id}" again and assert it returns a 404 status 
     code (this proves the delete actually worked)
   - `def test_delete_nonexistent_contact_returns_404():` -- DELETE
     "/contacts/999999", assert status_code == 404

## Run it

From INSIDE the `exercise_02/` folder:

    pytest -v

All 6 tests should PASS. If you re-run pytest multiple times, data
accumulates in test.db across runs (each run adds more contacts) --
that's expected here since we didn't add cleanup logic. If a test
seems to behave oddly after several runs, delete test.db and re-run.