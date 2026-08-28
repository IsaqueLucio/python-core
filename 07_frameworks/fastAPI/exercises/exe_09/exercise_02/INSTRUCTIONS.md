# Exercise 2: JWT tokens + a protected endpoint

## Goal
Add the SECOND half of authentication on top of exercise 1's password
hashing: issue a JWT on successful login, and protect an endpoint so
it only works with a valid token.

## Structure to build

    exercise_02/
    ├── database.py    (same generic file, copy it)
    ├── models.py
    ├── schemas.py
    ├── security.py    (password hashing, same as exercise_01, copy it)
    ├── auth.py         (NEW: JWT creation/verification)
    └── main.py

## Instructions

1. `models.py`, and the password-hashing parts of `security.py`: same
   as exercise_01 (copy them, but rename the model/table to whatever
   fits -- suggestion: keep `Account`/`accounts` for consistency).

2. In `schemas.py`, in addition to AccountCreate/AccountOut, add:
   - `Token` (output): access_token (str), token_type (str = "bearer")

3. In `auth.py` (NEW file):
   - `SECRET_KEY = "change-this-in-a-real-project"` (module-level
     constant)
   - `ALGORITHM = "HS256"`
   - `ACCESS_TOKEN_EXPIRE_MINUTES = 30`
   - `def create_access_token(data: dict) -> str:` -- copy the pattern
     from theory/09_auth/auth.py (copy expire time logic + jwt.encode)
   - `def decode_access_token(token: str) -> str | None:` -- same
     pattern, returns the username from the "sub" claim, or None if
     invalid (catch JWTError)

4. In `main.py`:
   - `oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")`
   - `POST "/register"`: same as exercise_01
   - `POST "/login"` (response_model=Token): use
     `OAuth2PasswordRequestForm = Depends()` (NOT a Pydantic model
     this time -- it reads FORM fields, not JSON). Verify credentials
     the same way as exercise_01, then call create_access_token(data={"sub": account.email})
     and return a Token.
   - `get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db))`:
     decode the token, raise HTTPException(401, "Invalid or expired
     token") if it fails, look up the account, raise
     HTTPException(401, "Account not found") if missing, otherwise
     return the account.
   - `GET "/me"` (response_model=AccountOut) using
     `Depends(get_current_user)`: return the current account.

## Run it

From INSIDE the `exercise_02/` folder:

    uvicorn main:app --reload

## Test in http://127.0.0.1:8000/docs

    1. POST /register with an email + password -> works
    2. POST /login -- IMPORTANT: in Swagger, this form now shows
       separate "username" and "password" fields (not a JSON body) --
       type your email in "username". You'll get back an access_token.
    3. GET /me WITHOUT authorizing -> 401
    4. Click the green "Authorize" button at the top of /docs, paste
       your access_token (or just the username/password -- Swagger's
       OAuth2 flow handles it), then GET /me again -> should return
       your account
    5. Wait 30+ minutes (or temporarily change
       ACCESS_TOKEN_EXPIRE_MINUTES to 1 to test faster) and try /me
       again with the old token -> 401 (expired)
