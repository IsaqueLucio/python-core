"""
See ../INSTRUCTIONS.md for the full task description.
"""

from fastapi import APIRouter, HTTPException

# TODO: create the router with prefix="/books" and tags=["books"]
router = APIRouter(prefix="/books", tags=["books"])

# TODO: create the `books` list with at least 4 sample books
# each with "id", "title", "available"
books = [
    {"id": 1, "title": "The Hobbit", "available": True},
    {"id": 2, "title": "1984", "available": False},
    {"id": 3, "title": "Pride and Prejudice", "available": True},
    {"id": 4, "title": "The Great Gatsby", "available": True},
]

# TODO: GET "" endpoint (becomes /books) returning the full list
@router.get("")
def get_books():
    return books

# TODO: GET "/{book_id}" endpoint (becomes /books/{book_id})
# raise HTTPException(404, "Book not found") if missing
@router.get("/{book_id}")
def get_book_by_id(book_id: int):
    for book in books:
        if book["id"] == book_id:
            return book
    raise HTTPException (status_code=404, detail="Book not found")
