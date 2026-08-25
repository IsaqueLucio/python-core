"""
See ../INSTRUCTIONS.md for the full task description.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import models
from database import get_db
from schemas import BookCreate, BookOut

# TODO: create the router with prefix="/books" and tags=["books"]
router = APIRouter(prefix="/books", tags=["books"])

# TODO: POST "" endpoint (becomes /books), response_model=BookOut
# first check the given author_id exists:
#   db.query(models.Author).filter(models.Author.id == book.author_id).first()
# raise HTTPException(404, "Author not found") if it doesn't
# otherwise create a models.Book, add/commit/refresh, return it
@router.post("", response_model=BookOut)
def post_book(book: BookCreate, db: Session = Depends(get_db)):
    author_exists = db.query(models.Author).filter(models.Author.id == book.author_id).first()
    if author_exists is None:
        raise HTTPException(status_code=404, detail="Author not found.")
    new_book = models.Book(**book.model_dump())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book

# TODO: GET "" endpoint (becomes /books), response_model=list[BookOut]
# return db.query(models.Book).all()
@router.get("", response_model = list[BookOut])
def get_books(db: Session = Depends(get_db)):
    books = db.query(models.Book).all()
    if books is None:
        return {}
    return books
