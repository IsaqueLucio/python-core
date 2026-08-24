# Exercise 1: Basic router split

## Goal
Take a single-file API and split it into two routers, wired together
in main.py.

## Structure to build

    exercise_01/
    ├── main.py
    └── routers/
        ├── __init__.py   (empty file, already created for you)
        └── books.py

(You need to create `books.py` and fill in `main.py` -- both already
exist as stub files with TODOs.)

## Instructions

1. In `routers/books.py`:
   - Create `router = APIRouter(prefix="/books", tags=["books"])`
   - Create a module-level list `books` with at least 4 dicts, each
     with "id" (int), "title" (str), and "available" (bool).
   - Create `GET ""` (becomes `/books`) returning the full list.
   - Create `GET "/{book_id}"` (becomes `/books/{book_id}`) returning
     the matching book, or raising HTTPException(404, "Book not found").

2. In `main.py`:
   - Create the FastAPI app instance.
   - Import the `books` router module.
   - Call `app.include_router(books.router)`.

## Run it

From INSIDE the `exercise_01/` folder:

    uvicorn main:app --reload

## Test in http://127.0.0.1:8000/docs

    - GET /books           -> full list
    - GET /books/1          -> single book
    - GET /books/999        -> 404 Book not found
