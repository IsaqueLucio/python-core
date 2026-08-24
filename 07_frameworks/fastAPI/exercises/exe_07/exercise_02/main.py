"""
See INSTRUCTIONS.md for the full task description.
"""
from fastapi import FastAPI

# TODO: import the admin router module
from routers import admin

# TODO: create the FastAPI app instance
app = FastAPI(
    title="Learning FastAPI - Exercise 2: Router-level dependencies",
    description="""
        Practice protecting an ENTIRE router with a single dependency, instead
        of adding `Depends(...)` to every individual endpoint (which is what
        you'd have to do without this feature).
    """,
    version="0.1.0",
)

# TODO: include the admin router
app.include_router(admin.router)
