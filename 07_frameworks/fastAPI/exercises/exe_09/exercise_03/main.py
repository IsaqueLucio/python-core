"""
See INSTRUCTIONS.md for the full task description.
"""

from fastapi import FastAPI
from routers import admin, auth_router
from database import Base, engine

# TODO: create all tables
Base.metadata.create_all(bind=engine)

# TODO: create the FastAPI app instance
app = FastAPI(
    title="Learning FastAPI: Exercise 3",
    description="Authentication with JWT",
    version="0.1.0",
)

# TODO: import both router modules and include them
# from routers import auth_router, admin
app.include_router(admin.router)
app.include_router(auth_router.router)