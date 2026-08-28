"""
See ../INSTRUCTIONS.md for the full task description.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import models
from database import get_db
from routers.auth_router import get_current_user
from schemas import AccountOut

# TODO: define require_admin(current_user: models.Account = Depends(get_current_user))
# raise HTTPException(403, "Admin access required") if
# current_user.role != "admin", otherwise return current_user
def require_admin(current_user: models.Account = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user

# TODO: create the router with prefix="/admin", tags=["admin"],
# and dependencies=[Depends(require_admin)]
router = APIRouter(prefix="/admin", tags=["admin"], dependencies=[Depends(require_admin)])

# TODO: GET "/users" endpoint, response_model=list[AccountOut]
# return db.query(models.Account).all()
@router.get("/users", response_model=list[AccountOut])
def get_users(db: Session = Depends(get_db)):
    all_users = db.query(models.Account).all()
    return all_users