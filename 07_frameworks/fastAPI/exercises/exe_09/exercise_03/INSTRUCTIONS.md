# Exercise 3: Role-based access control + routers

## Goal
Combine everything: auth split across routers (topic 7), a `role`
field on the user, and a dependency that requires a SPECIFIC role
(chained on top of get_current_user, same pattern as topic 6,
exercise 3's require_admin).

## Structure to build

    exercise_03/
    ├── database.py     (same generic file, copy it)
    ├── models.py
    ├── schemas.py
    ├── security.py     (same as previous exercises, copy it)
    ├── auth.py          (same as exercise_02, copy it)
    ├── main.py
    └── routers/
        ├── __init__.py  (empty file, already created for you)
        ├── auth_router.py
        └── admin.py

## Instructions

1. In `models.py`:
   - `class Account(Base):` same as before, PLUS a new column:
     `role = Column(String, default="user")` (will hold "user" or
     "admin")

2. In `schemas.py`:
   - `AccountCreate` (input): email (str), password (str)
   - `AccountOut` (output): id (int), email (str), role (str) --
     still no password
   - `Token` (output): access_token (str), token_type (str = "bearer")

3. `security.py` and `auth.py`: same as exercise_02, copy them.

4. In `routers/auth_router.py` (register + login + get_current_user,
   moved out of main.py and into its own router, similar to how
   dependencies.py was shared in topic 7's exercise 3):
   - `router = APIRouter(tags=["auth"])`  (no prefix -- /register and
     /login should NOT be nested under anything)
   - `POST "/register"` (response_model=AccountOut): same logic as
     before, new accounts always start with role="user" (don't let
     the client choose their own role at registration -- that would
     be a security hole!)
   - `POST "/login"` (response_model=Token): same as exercise_02
   - `oauth2_scheme` and `get_current_user(...)`: same as exercise_02,
     but defined here so `admin.py` can import get_current_user from
     this module

5. In `routers/admin.py`:
   - `from routers.auth_router import get_current_user`
   - Define `require_admin(current_user: models.Account = Depends(get_current_user))`
     that raises HTTPException(403, "Admin access required") if
     `current_user.role != "admin"`, otherwise returns current_user
     (same chained-dependency pattern as topic 6, exercise 3)
   - `router = APIRouter(prefix="/admin", tags=["admin"], dependencies=[Depends(require_admin)])`
   - `GET "/users"` (response_model=list[AccountOut]): returns
     `db.query(models.Account).all()` -- only reachable by an admin,
     thanks to the router-level dependency (topic 7, exercise 2 style)

6. In `main.py`:
   - `Base.metadata.create_all(bind=engine)` + create the app
   - `from routers import auth_router, admin`
   - `app.include_router(auth_router.router)`
   - `app.include_router(admin.router)`

7. One manual step, since there's no endpoint to promote a user: after
   registering a user through the API, manually flip their role to
   "admin" directly in the database to test the admin-only endpoint.
   You can do this with any SQLite browser tool, or quickly via
   Python:
   ```python
   # run this once, in a separate throwaway script or a Python shell,
   # from inside the exercise_03 folder
   from database import SessionLocal
   import models

   db = SessionLocal()
   user = db.query(models.Account).filter(models.Account.email == "admin@example.com").first()
   user.role = "admin"
   db.commit()
   ```

## Run it

From INSIDE the `exercise_03/` folder:

    uvicorn main:app --reload

## Test in http://127.0.0.1:8000/docs

    - POST /register + POST /login as a normal user
    - GET /admin/users with that user's token -> 403 Admin access required
    - Promote that user to admin (step 7 above), log in again (tokens
      issued BEFORE the promotion won't reflect the new role only if
      you encode the role into the token -- here we look up the
      account fresh on every request, so even an old token still
      works after promotion)
    - GET /admin/users again -> should now work, listing every account
