# Exercise 2: Router-level dependencies

## Goal
Practice protecting an ENTIRE router with a single dependency, instead
of adding `Depends(...)` to every individual endpoint (which is what
you'd have to do without this feature).

## Structure to build

    exercise_02/
    ├── main.py
    └── routers/
        ├── __init__.py   (empty file, already created for you)
        └── admin.py

## Instructions

1. In `routers/admin.py`:
   - Create a dependency function `verify_admin_key(x_admin_key: str = Header(...))`
     that raises HTTPException(401, "Invalid admin key") if
     `x_admin_key != "letmein"`.
   - Create the router like this:

     router = APIRouter(
         prefix="/admin",
         tags=["admin"],
         dependencies=[Depends(verify_admin_key)],
     )

     The `dependencies=[...]` list applied at the ROUTER level means
     EVERY endpoint below runs `verify_admin_key` first, automatically
     -- you don't need to repeat `Depends(verify_admin_key)` on each one.

   - Create a module-level list `logs` with at least 5 short strings.
   - Create `GET "/logs"` (becomes `/admin/logs`) returning the list.
     Notice: this endpoint's signature does NOT need
     `Depends(verify_admin_key)` in its parameters -- the router
     already guarantees it runs first.
   - Create `DELETE "/logs"` (becomes `/admin/logs`) that clears the
     list (`logs.clear()`) and returns `{"message": "Logs cleared"}`.
     Also does NOT need Depends in its own signature.

2. In `main.py`:
   - Create the FastAPI app instance.
   - Import the `admin` router module.
   - Call `app.include_router(admin.router)`.

## Run it

From INSIDE the `exercise_02/` folder:

    uvicorn main:app --reload

## Test in http://127.0.0.1:8000/docs

    - GET /admin/logs without header X-Admin-Key    -> 401
    - GET /admin/logs with header X-Admin-Key: letmein -> works
    - DELETE /admin/logs with header X-Admin-Key: letmein -> clears it
