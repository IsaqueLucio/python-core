"""
See INSTRUCTIONS.md for the full task description.
"""

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import models
from database import Base, engine, get_db
from schemas import ContactCreate, ContactOut

# TODO: create all tables
Base.metadata.create_all(bind=engine)

# TODO: create the FastAPI app instance
app = FastAPI()

# TODO: POST "/contacts" endpoint, response_model=ContactOut
@app.post("/contacts", response_model=ContactOut)
def post_contacts(contact: ContactCreate, db: Session = Depends(get_db)):
    new_contact = models.Contact(**contact.model_dump())
    db.add(new_contact)
    db.commit()
    db.refresh(new_contact)
    return new_contact

# TODO: GET "/contacts" endpoint, response_model=list[ContactOut]
@app.get("/contacts", response_model = list[ContactOut])
def get_contacts(db: Session = Depends(get_db)):
    return db.query(models.Contact).all()

# TODO: GET "/contacts/{contact_id}" endpoint, response_model=ContactOut
@app.get("/contacts/{contact_id}", response_model=ContactOut)
def get_contact_by_id(contact_id: int, db: Session = Depends(get_db)):
    item = db.query(models.Contact).filter(models.Contact.id == contact_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Contact not found.")
    return item

# TODO: DELETE "/contacts/{contact_id}" endpoint
# find by id, raise 404 if missing, delete, return
# {"message": "Contact deleted"}
@app.delete("/contacts/{contact_id}")
def delete_by_id(contact_id: int, db: Session = Depends(get_db)):
    item = db.query(models.Contact).filter(models.Contact.id == contact_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Contact not found.")
    db.delete(item)
    db.commit()
    return {"message": "Contact deleted"}

