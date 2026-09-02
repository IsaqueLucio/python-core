# Exercise 3: Testing authenticated endpoints

## Goal
Combine topic 9 (auth) with this topic: write tests that register a
user, log in to get a real token, and use it to access a protected
endpoint -- plus tests confirming that missing/invalid tokens are
rejected.

## Structure to build

    exercise_03/
    ├── database.py    (same generic file, copy it)
    ├── models.py
    ├── schemas.py
    ├── security.py    (password hashing, same as topic 9, copy it)
    ├── auth.py         (JWT logic, same as topic 9 exercise_02, copy it)
    ├── main.py
    └── test_main.py

## Instructions

1. `models.py`, `schemas.py`, `security.py`, `auth.py`: reuse the
   SAME patterns from topic 9, exercise 2 (Account model with email +
   hashed_password, AccountCreate/AccountOut/Token schemas, password
   hashing, JWT creation/decoding). Copy them over and adjust naming
   if needed.

2. In `main.py`: same as topic 9, exercise 2 -- POST /register,
   POST /login (using OAuth2PasswordRequestForm), get_current_user
   dependency, and a protected `GET "/me"` endpoint
   (response_model=AccountOut).

3. In `test_main.py`:
   - Set up the SAME test-database override pattern as exercise 2
     (separate sqlite:///./test.db, override_get_db,
     app.dependency_overrides[get_db] = override_get_db)
   - `client = TestClient(app)`

   - `def test_register_new_account():` -- POST /register with a new
     email/password, assert status_code == 200, assert the response
     has no "password" field (response_model doing its job, same
     check as topic 5's exercises)

   - `def test_register_duplicate_email_fails():` -- POST /register
     TWICE with the same email, assert the SECOND attempt has
     status_code == 409

   - `def test_login_with_correct_credentials():` -- register a NEW
     account (use a different email than the tests above -- test
     functions can run in any order, so never assume another test's
     data exists), then POST /login using
     `client.post("/login", data={"username": email, "password": password})`
     (note: `data=`, not `json=` -- OAuth2PasswordRequestForm reads
     FORM fields, exactly like topic 9's exercise 2 mentioned).
     Assert status_code == 200, assert "access_token" is present in
     the response.

   - `def test_login_with_wrong_password_fails():` -- register an
     account, then try to log in with the WRONG password, assert
     status_code == 401.

   - `def test_protected_endpoint_without_token_fails():` -- GET
     "/me" with NO Authorization header at all, assert status_code == 401.

   - `def test_protected_endpoint_with_valid_token_succeeds():` --
     register an account, log in to get a real token, then GET "/me"
     passing the token as a header:
     `client.get("/me", headers={"Authorization": f"Bearer {token}"})`
     assert status_code == 200, assert the response "email" matches
     the account you registered.

## Run it

From INSIDE the `exercise_03/` folder:

    pytest -v

All 6 tests should PASS.

## A note on test independence

Notice every test that needs an account REGISTERS ITS OWN, with a
unique email, instead of relying on a shared "the user from the
earlier test still exists" assumption. This matters because pytest
doesn't guarantee execution order between test FILES, and even within
one file, a test should be understandable and correct on its own,
without needing to know what ran before it. This is a general testing
principle, not a FastAPI-specific one -- it applies to Java/JUnit
tests too.
