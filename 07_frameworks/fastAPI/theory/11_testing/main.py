"""
A small API to test: create and list items. Nothing test-specific
lives here -- this file has no idea it's being tested. That's the
whole point: your application code stays clean, tests live separately.
"""

from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

import models
from database import Base, engine, get_db
from schemas import ItemCreate, ItemOut

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Learning FastAPI",
    description="Automated testing example",
    version="0.1.0",
)


@app.post("/items", response_model=ItemOut)
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    new_item = models.Item(**item.model_dump())
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item


@app.get("/items", response_model=list[ItemOut])
def list_items(db: Session = Depends(get_db)):
    return db.query(models.Item).all()

