from fastapi import APIRouter, HTTPException, Depends
from app.schemas import UserCreate, UserOut, Token
from fastapi.security import OAuth2PasswordRequestForm
import app.models
from sqlalchemy.orm import Session
from app.auth import create_access_token
from app.database import get_db
from app.security import hash_password, verify_password

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserOut, status_code=201)
def register(user: UserCreate, db: Session = Depends(get_db)):
    exist_email = db.query(app.models.User).filter(app.models.User.email == user.email).first()
    exist_username = db.query(app.models.User).filter(app.models.User.username == user.username).first()
    if exist_email:
        raise HTTPException(status_code=409, detail="The email is already registered.")
    if exist_username:
        raise HTTPException(status_code=409, detail="The username is already registered.")
    new_user = app.models.User(
        username = user.username,
        email = user.email,
        hashed_password = hash_password(user.password.get_secret_value())
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(app.models.User).filter(app.models.User.email == form_data.username).first()
    if user is None or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect username or password.")
    access_token = create_access_token(data={"sub": user.email})
    return Token(access_token=access_token)


