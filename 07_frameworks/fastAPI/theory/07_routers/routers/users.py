"""
All /users endpoints live here, isolated from the rest of the app.
This file has NO idea about items, or any other domain -- that's the
whole point of splitting by router.
"""

from fastapi import APIRouter, HTTPException

# prefix="/users" -> every route below is relative to /users
# tags=["users"] -> groups these routes together in /docs
router = APIRouter(prefix="/users", tags=["users"])

users = [
    {"id": 1, "username": "isaque"},
    {"id": 2, "username": "maria"},
]


# This becomes GET /users (the prefix is added automatically)
@router.get("")
def list_users():
    return users


# This becomes GET /users/{user_id}
@router.get("/{user_id}")
def get_user(user_id: int):
    for user in users:
        if user["id"] == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")
