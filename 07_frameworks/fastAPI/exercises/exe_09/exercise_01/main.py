"""
See INSTRUCTIONS.md for the full task description.
"""

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import models
from database import Base, engine, get_db
from schemas import AccountCreate, AccountOut
from security import hash_password, verify_password

# TODO: create all tables
Base.metadata.create_all(bind=engine)
# TODO: create the FastAPI app instance
app = FastAPI(
    title="Learning FastAPI: Exercise 01",
    description="Authentication with JWT",
    version="0.1.0",
)

# TODO: POST "/register" endpoint, response_model=AccountOut
# raise 409 if email already exists, otherwise hash the password
# and save the account
@app.post("/register", response_model=AccountOut)
def post_register(account: AccountCreate, db: Session = Depends(get_db)):
    exists = db.query(models.Account).filter(models.Account.email == account.email).first()
    if exists:
        raise HTTPException(status_code=409, detail="The email already exists.")
    new_account = models.Account(
        email = account.email,
        hashed_password = hash_password(account.password)
    )
    db.add(new_account)
    db.commit()
    db.refresh(new_account)
    return new_account

# TODO: POST "/login" endpoint (receives AccountCreate)
# look up by email, verify password, raise 401 with the SAME message
# for "not found" and "wrong password", otherwise return a welcome message
@app.post("/login")
def post_login(account: AccountCreate, db: Session = Depends(get_db)):
    user = db.query(models.Account).filter(models.Account.email == account.email).first()
    if user is None or not verify_password(account.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    return {"message": "Successfully logged in! Welcome."}