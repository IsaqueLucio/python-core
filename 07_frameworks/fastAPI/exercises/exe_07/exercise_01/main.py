"""
See INSTRUCTIONS.md for the full task description.
"""

from fastapi import FastAPI

# TODO: import the books router module
from routers import books

# TODO: create the FastAPI app instance
app = FastAPI(
    title="Learning FastAPI - Exercise 1: Basic router split",
    description="Take a single-file API and split it into two routers, wired together in main.py.",
    version="0.1.0",
)

# TODO: include the books router
app.include_router(books.router)

@app.get("/")
def read_root():
    return {"message": "See /docs for all available endpoints"}