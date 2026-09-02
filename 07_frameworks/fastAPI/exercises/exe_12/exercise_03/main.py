"""
See INSTRUCTIONS.md for the full task description.
"""

from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

import models
from database import Base, engine, get_db
from schemas import BookCreate, BookOut

# TODO: create all tables
Base.metadata.create_all(bind=engine)

# TODO: create the FastAPI app instance
app = FastAPI()

# TODO: POST "/books" endpoint, response_model=BookOut
@app.post("/books", response_model = BookOut)
def post_books(book: BookCreate, db: Session = Depends(get_db)):
    new_book = models.Book(
        title = book.title,
        author = book.author
    )
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book

# TODO: GET "/books" endpoint, response_model=list[BookOut]
@app.get("/books", response_model=list[BookOut])
def get_books(db: Session = Depends(get_db)):
    books = db.query(models.Book).all()
    return books

