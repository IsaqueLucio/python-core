"""
See ../INSTRUCTIONS.md for the full task description.
"""

from fastapi import APIRouter, Depends

# TODO: import get_current_user from the dependencies module
from dependencies import get_current_user

# TODO: create the router with prefix="/carts" and tags=["carts"]
router = APIRouter(
    prefix="/carts",
    tags=["carts"]
)

# TODO: create the `carts_by_user` dict (starts empty)
carts_by_user = {}

# TODO: POST "/items" endpoint
# query param: item (str)
# dependency: user (dict, via Depends(get_current_user))
# append item to carts_by_user[user["username"]], creating the list
# if needed, then return the updated cart list
@router.post("/items")
def post_items(item: str, user: dict = Depends(get_current_user)):
    username = user["username"]
    if username not in carts_by_user:
        carts_by_user[username] = []
    carts_by_user[username].append(item)
    return carts_by_user[username]

# TODO: GET "" endpoint (becomes /carts)
# dependency: user (dict, via Depends(get_current_user))
# return the calling user's cart, or an empty list if none yet
@router.get("")
def get_carts(user: dict = Depends(get_current_user)):
    username = user["username"]
    if username not in carts_by_user:
        return []
    return carts_by_user[username]