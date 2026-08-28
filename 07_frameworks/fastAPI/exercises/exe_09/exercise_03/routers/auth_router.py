"""
See ../INSTRUCTIONS.md for the full task description.

Registration, login, and get_current_user all live here so that
OTHER routers (like admin.py) can import get_current_user without
depending on main.py.
"""

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

import models
from auth import create_access_token, decode_access_token
from database import get_db
from schemas import AccountCreate, AccountOut, Token
from security import hash_password, verify_password

# TODO: create the router with tags=["auth"] (no prefix)
router = APIRouter(tags=["auth"])

# TODO: create oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# TODO: POST "/register" endpoint, response_model=AccountOut
# new accounts always start with role="user" -- never let the client
# set their own role at registration time
@router.post("/register", response_model=AccountOut)
def post_register(account: AccountCreate, db: Session = Depends(get_db)):
    exists = db.query(models.Account).filter(models.Account.email == account.email).first()
    if exists:
        raise HTTPException(status_code=409, detail="The email is already registred.")
    new_account = models.Account(
        email = account.email,
        hashed_password = hash_password(account.password),
        role = "user"
    )
    db.add(new_account)
    db.commit()
    db.refresh(new_account)
    return new_account

# TODO: POST "/login" endpoint, response_model=Token
# form_data: OAuth2PasswordRequestForm = Depends()
@router.post("/login", response_model=Token)
def post_login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.Account).filter(models.Account.email == form_data.username).first()
    if user is None or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect username or password.")
    access_token = create_access_token(data={"sub": user.email})
    return Token(access_token=access_token)

# TODO: define get_current_user(token: str = Depends(oauth2_scheme),
# db: Session = Depends(get_db))
# decode token, raise 401 if invalid, look up account, raise 401 if
# missing, return the account
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> models.Account:
    username = decode_access_token(token)
    if username is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    user = db.query(models.Account).filter(models.Account.email == username).first()
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user
