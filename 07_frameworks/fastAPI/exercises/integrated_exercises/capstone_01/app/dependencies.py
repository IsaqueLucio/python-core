from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
import app.models
from sqlalchemy.orm import Session
from app.auth import decode_access_token
from app.database import get_db
from fastapi import Query

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    username = decode_access_token(token)
    if username is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    user = db.query(app.models.User).filter(app.models.User.email == username).first()
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user

def require_admin(current_user: app.models.User = Depends(get_current_user)) -> app.models.User:
    if current_user.role != app.models.UserRole.ADMIN:
        raise HTTPException(
            status_code=403,
            detail="The user is not an admin."
        )
    return current_user

def get_pagination(
        skip: int = Query(0, ge=0, description="Number of records to skip"),
        limit: int = Query(10, ge=1, le=100, description="Limit of records per page")):
    return {"skip": skip, "limit": limit}