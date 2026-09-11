import app.models
from app.dependencies import require_admin
from app.database import get_db
from app.schemas import UserOut
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

router = APIRouter(prefix= "/admin" ,tags=["admin"], dependencies=[Depends(require_admin)])

@router.get("/users", response_model=list[UserOut])
def get_users(db: Session = Depends(get_db)):
    users = db.query(app.models.User).all()
    return users

@router.delete("/users/{user_id}", status_code=204)
def delete_user(user_id: int,
                db: Session = Depends(get_db),
                current_admin: app.models.User = Depends(require_admin)):
    user = db.query(app.models.User).filter(app.models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    if user_id == current_admin.id:
        raise HTTPException(status_code=409, detail="Cannot delete current administrator.")
    db.delete(user)
    db.commit()