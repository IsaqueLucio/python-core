"""
Wires everything together: creates the tables (if they don't exist
yet), and exposes CRUD endpoints backed by a real database instead of
an in-memory list.
"""

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import models
from database import Base, engine, get_db
from schemas import BookCreate, BookOut

# This creates every table declared in models.py, but ONLY if it
# doesn't already exist. Safe to call every time the app starts.
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Learning FastAPI",
    description="Database example with SQLAlchemy",
    version="0.1.0",
)


@app.post("/books", response_model=BookOut)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    # Convert the Pydantic input model into an ORM model instance.
    new_book = models.Book(**book.model_dump())
    db.add(new_book)       # stage the insert
    db.commit()             # actually save it
    db.refresh(new_book)    # reload it, so new_book.id is populated
    return new_book


@app.get("/books", response_model=list[BookOut])
def list_books(db: Session = Depends(get_db)):
    # .query(Model).all() is the SQLAlchemy equivalent of
    # "SELECT * FROM books" -- roughly like a JPA findAll().
    return db.query(models.Book).all()


@app.get("/books/{book_id}", response_model=BookOut)
def get_book(book_id: int, db: Session = Depends(get_db)):
    # .filter(...).first() is roughly like findById() -- returns the
    # first match, or None if nothing matches.
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book
