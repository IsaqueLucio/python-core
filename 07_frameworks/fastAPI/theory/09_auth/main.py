"""
Wires everything together: register, login, and a protected endpoint.
"""

from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

import models
from auth import create_access_token, decode_access_token, hash_password, verify_password
from database import Base, engine, get_db
from schemas import Token, UserCreate, UserOut

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Learning FastAPI",
    description="Authentication with JWT / OAuth2",
    version="0.1.0",
)

# tokenUrl="login" tells the /docs UI (and any OAuth2 client) WHERE to
# send username/password to get a token. It does NOT create that
# route for you -- you still define POST /login yourself below.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


@app.post("/register", response_model=UserOut)
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter(models.User.username == user.username).first()
    if existing:
        raise HTTPException(status_code=409, detail="Username already taken")

    new_user = models.User(
        username=user.username,
        hashed_password=hash_password(user.password),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    OAuth2PasswordRequestForm expects form fields named "username"
    and "password" (not JSON!) -- this is part of the OAuth2 standard
    this pattern follows. The /docs "Authorize" button fills this in
    for you automatically.
    """
    user = db.query(models.User).filter(models.User.username == form_data.username).first()

    if user is None or not verify_password(form_data.password, user.hashed_password):
        # Deliberately vague message: never reveal WHICH field was
        # wrong (username vs password) -- that helps attackers.
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    access_token = create_access_token(data={"sub": user.username})
    return Token(access_token=access_token)


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> models.User:
    """
    This is a dependency (topic 6) that any protected endpoint can
    use. It decodes the token, looks up the user, and either returns
    it or raises 401 -- the same "dependency that validates and
    raises errors" pattern from topic 6, exercise 2.
    """
    username = decode_access_token(token)
    if username is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user = db.query(models.User).filter(models.User.username == username).first()
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")

    return user


@app.get("/me", response_model=UserOut)
def read_own_profile(current_user: models.User = Depends(get_current_user)):
    """
    A protected endpoint: FastAPI won't even run this function's body
    unless get_current_user() succeeds first.
    """
    return current_user
