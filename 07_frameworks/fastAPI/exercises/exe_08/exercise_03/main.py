"""
See INSTRUCTIONS.md for the full task description.
"""

from fastapi import FastAPI
from routers import authors, books
from database import Base, engine

# TODO: create all tables
Base.metadata.create_all(bind=engine)

# TODO: create the FastAPI app instance
app = FastAPI()

# TODO: import both router modules and include them
# from routers import authors, books
app.include_router(authors.router)
app.include_router(books.router)