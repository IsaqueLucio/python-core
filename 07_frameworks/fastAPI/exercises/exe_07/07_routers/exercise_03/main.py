"""
See INSTRUCTIONS.md for the full task description.
"""

from fastapi import FastAPI

# TODO: import both router modules
from routers import carts, wishlists

# TODO: create the FastAPI app instance
app = FastAPI(
    title="Learning FastAPI - Exercise 3: Multi-router project with shared dependencies",
    description="""
        Put everything from this topic together in a slightly more realistic
        layout: two routers, PLUS a separate `dependencies.py` file for shared
        logic that both routers use (instead of each router redefining its
        own auth check). This is the closest thing so far to the layered
        structure you said you want for your final module project.
    """,
    version="0.1.0",
)

# TODO: include both routers
app.include_router(carts.router)
app.include_router(wishlists.router)