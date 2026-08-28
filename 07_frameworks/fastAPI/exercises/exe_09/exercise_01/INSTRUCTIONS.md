# Exercise 1: Password hashing (no JWT yet)

## Goal
Isolate the FIRST half of authentication: registering a user with a
safely hashed password, and checking a login attempt against it --
without tokens yet. This lets you focus on passlib alone before
adding JWT on top in the next exercise.

## Structure to build

    exercise_01/
    ├── database.py   (same generic file from topic 8, copy it)
    ├── models.py
    ├── schemas.py
    └── main.py

## Instructions

1. In `models.py`:
   - Define `class Account(Base):` with `__tablename__ = "accounts"`
   - Columns: id (Integer, primary_key, index), email (String,
     unique=True, nullable=False), hashed_password (String,
     nullable=False)

2. In `schemas.py`:
   - `AccountCreate` (input): email (str), password (str)
   - `AccountOut` (output): id (int), email (str) -- no password
     field at all, with `model_config = ConfigDict(from_attributes=True)`

3. Create a new file `security.py` with:
   - `from passlib.context import CryptContext`
   - `pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")`
   - `def hash_password(plain_password: str) -> str:` using
     `pwd_context.hash(...)`
   - `def verify_password(plain_password: str, hashed_password: str) -> bool:`
     using `pwd_context.verify(...)`

4. In `main.py`:
   - `Base.metadata.create_all(bind=engine)` + create the app
   - `POST "/register"` (response_model=AccountOut): receives an
     AccountCreate, raises HTTPException(409, "Email already
     registered") if the email is already in the database, otherwise
     hashes the password (never store the plain one!) and saves the
     account
   - `POST "/login"` that receives an AccountCreate (reusing it here
     just for convenience -- email + password) and:
     - looks up the account by email
     - if not found OR verify_password fails, raises
       HTTPException(401, "Invalid credentials")
     - otherwise returns `{"message": f"Welcome back, {account.email}"}`

     Note: on purpose, use the EXACT SAME error message/status for
     "email not found" and "wrong password" -- never let an attacker
     figure out whether an email exists in your system just from the
     error message.

## Run it

From INSIDE the `exercise_01/` folder:

    uvicorn main:app --reload

## Test in http://127.0.0.1:8000/docs

    POST /register
    Body: {"email": "test@example.com", "password": "mypassword123"}
    -> should work, response has NO password field

    POST /register (same email again)
    -> 409 Email already registered

    POST /login
    Body: {"email": "test@example.com", "password": "mypassword123"}
    -> {"message": "Welcome back, test@example.com"}

    POST /login
    Body: {"email": "test@example.com", "password": "wrongpassword"}
    -> 401 Invalid credentials

    POST /login
    Body: {"email": "nobody@example.com", "password": "anything"}
    -> 401 Invalid credentials (SAME message as above -- don't reveal
       which part was wrong)
