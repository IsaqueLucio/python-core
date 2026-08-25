"""
See ../INSTRUCTIONS.md for the full task description.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import models
from database import get_db
from schemas import AuthorCreate, AuthorOut

# TODO: create the router with prefix="/authors" and tags=["authors"]
router = APIRouter(prefix="/authors", tags=["authors"])

# TODO: POST "" endpoint (becomes /authors), response_model=AuthorOut
# create a models.Author, add/commit/refresh, return it
@router.post("", response_model=AuthorOut)
def post_author(author: AuthorCreate, db: Session = Depends(get_db)):
    new_author = models.Author(**author.model_dump())
    db.add(new_author)
    db.commit()
    db.refresh(new_author)
    return new_author

# TODO: GET "" endpoint (becomes /authors), response_model=list[AuthorOut]
# return db.query(models.Author).all()
@router.get("", response_model=list[AuthorOut])
def get_authors(db: Session = Depends(get_db)):
    authors = db.query(models.Author).all()
    if authors is None:
        return {}
    return authors

# TODO: GET "/{author_id}" endpoint (becomes /authors/{author_id})
# response_model=AuthorOut
# find by id, raise HTTPException(404, "Author not found") if missing
@router.get("/{author_id}", response_model=AuthorOut)
def get_author(author_id: int, db: Session = Depends(get_db)):
    author = db.query(models.Author).filter(models.Author.id == author_id).first()
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return author
