"""
main.py is now just the "assembly point": it creates the app and
plugs in every router. No endpoint logic lives here directly anymore.

Compare this to Spring Boot's @SpringBootApplication class: it doesn't
contain your business endpoints either, it just bootstraps the app and
lets component scanning wire everything else in. Here, YOU do the
wiring explicitly with include_router (no "magic" auto-discovery).
"""

from fastapi import FastAPI

from routers import items, users

app = FastAPI(
    title="Learning FastAPI",
    description="Routers example -- endpoints split across files",
    version="0.1.0",
)

# Each router gets "mounted" onto the main app. From this point on,
# GET /users, GET /users/{id}, GET /items, GET /items/{id} all work
# exactly as if they'd been defined directly on `app`.
app.include_router(users.router)
app.include_router(items.router)


@app.get("/")
def read_root():
    return {"message": "See /docs for all available endpoints"}
