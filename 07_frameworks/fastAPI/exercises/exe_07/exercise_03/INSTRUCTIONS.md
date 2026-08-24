# Exercise 3: Multi-router project with shared dependencies

## Goal
Put everything from this topic together in a slightly more realistic
layout: two routers, PLUS a separate `dependencies.py` file for shared
logic that both routers use (instead of each router redefining its
own auth check). This is the closest thing so far to the layered
structure you said you want for your final module project.

## Structure to build

    exercise_03/
    ├── main.py
    ├── dependencies.py
    └── routers/
        ├── __init__.py    (empty file, already created for you)
        ├── carts.py
        └── wishlists.py

## Instructions

1. In `dependencies.py` (a NEW file, at the same level as main.py --
   not inside routers/):
   - Define `get_current_user(x_user: str = Header(...))` that simply
     returns `{"username": x_user}` (no validation needed here, this
     is a simplified stand-in for real auth, which comes in the next
     topic).

2. In `routers/carts.py`:
   - Import `get_current_user` from the `dependencies` module
     (`from dependencies import get_current_user`).
   - Create `router = APIRouter(prefix="/carts", tags=["carts"])`.
   - Create a module-level dict `carts_by_user = {}` (maps username ->
     list of item names).
   - Create `POST "/items"` with a query param `item: str`, and
     `user: dict = Depends(get_current_user)`. It should append `item`
     to `carts_by_user[user["username"]]` (creating the list if the
     user has no cart yet) and return the updated cart list.
   - Create `GET ""` (becomes `/carts`) with
     `user: dict = Depends(get_current_user)`, returning the calling
     user's cart (or an empty list if they have none yet).

3. In `routers/wishlists.py`:
   - Same pattern as carts.py, but for wishlists: import
     `get_current_user`, create a router with `prefix="/wishlists"`,
     a `wishlists_by_user = {}` dict, a `POST "/items"` and a
     `GET ""` endpoint. This reinforces that dependencies.py is
     reused across MULTIPLE routers, not just one.

4. In `main.py`:
   - Create the FastAPI app instance.
   - Import both router modules and include both with
     `app.include_router(...)`.

## Run it

From INSIDE the `exercise_03/` folder:

    uvicorn main:app --reload

## Test in http://127.0.0.1:8000/docs

    - POST /carts/items?item=Keyboard with header X-User: isaque
      -> {"cart or list showing Keyboard"}
    - GET /carts with header X-User: isaque
      -> shows the cart for that user
    - POST /wishlists/items?item=Monitor with header X-User: isaque
      -> works independently of the cart
    - Try a DIFFERENT X-User header value and confirm the cart/wishlist
      are separate per user
