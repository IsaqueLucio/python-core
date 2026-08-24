# Topic: Routers (APIRouter) — organizing endpoints across files

Up until now, every endpoint lived in a single .py file. That's fine
for learning, but a real API with dozens of endpoints in one file
becomes unreadable fast. `APIRouter` lets you split endpoints into
separate files by domain (users, products, orders...) and then plug
them all into the main `FastAPI()` app.

Coming from Spring Boot, think of it this way:
- APIRouter                  -> like a @RestController class
- router = APIRouter(prefix=...) -> like the base path in
                                     @RequestMapping("/users") on the
                                     class itself
- app.include_router(router) -> like Spring auto-registering every
                                 @Controller bean into the app context,
                                 except here YOU explicitly wire it up
                                 in main.py

## This folder's structure

    theory/07_routers/
    ├── main.py              # creates the app, includes the routers
    └── routers/
        ├── __init__.py      # (empty, just marks it as a package)
        ├── users.py         # all /users endpoints
        └── items.py         # all /items endpoints

## How to run this example

From inside `theory/07_routers/`:

    uvicorn main:app --reload

(Notice the import path is just `main:app` now, not
`theory.07_routers.main:app` — you run uvicorn from WITHIN the
project folder, the same way you'll run your real FastAPI projects
from now on.)

## Key takeaways

1. `APIRouter()` behaves almost exactly like `FastAPI()` for defining
   routes (`@router.get(...)`, `@router.post(...)`, etc.) — it's a
   "mini app" that gets merged into the main one later.
2. `prefix="/users"` means you don't repeat "/users" in every route
   inside that file — `@router.get("/{user_id}")` becomes
   `/users/{user_id}` once included.
3. `tags=["users"]` groups the routes together in the /docs Swagger
   UI, purely for organization/readability.
4. `app.include_router(router)` in main.py is the ONE place where all
   the pieces get wired together — similar to how Spring Boot
   auto-discovers your @Controller classes, except explicit here.
5. Dependencies (Depends) can also be applied to an ENTIRE router at
   once, not just to individual endpoints — useful for "all these
   routes require login", see the exercises for this pattern.
