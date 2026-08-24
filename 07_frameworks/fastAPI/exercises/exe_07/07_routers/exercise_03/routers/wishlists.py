"""
See ../INSTRUCTIONS.md for the full task description.

Same pattern as carts.py -- notice how get_current_user is reused
here too, without being redefined.
"""

from fastapi import APIRouter, Depends

# TODO: import get_current_user from the dependencies module
from dependencies import get_current_user

# TODO: create the router with prefix="/wishlists" and tags=["wishlists"]
router = APIRouter(
    prefix="/wishlists",
    tags=["wishlists"]
)

# TODO: create the `wishlists_by_user` dict (starts empty)
wishlists_by_user = {}

# TODO: POST "/items" endpoint
# query param: item (str)
# dependency: user (dict, via Depends(get_current_user))
# append item to wishlists_by_user[user["username"]], creating the
# list if needed, then return the updated wishlist
@router.post("/items")
def post_items(item: str, user: dict = Depends(get_current_user)):
    username = user["username"]
    if username not in wishlists_by_user:
        wishlists_by_user[username] = []
    wishlists_by_user[username].append(item)
    return wishlists_by_user[username]

# TODO: GET "" endpoint (becomes /wishlists)
# dependency: user (dict, via Depends(get_current_user))
# return the calling user's wishlist, or an empty list if none yet
@router.get("")
def get_wishlist(user: dict = Depends(get_current_user)):
    username = user["username"]
    if username not in wishlists_by_user:
        return []
    return wishlists_by_user[username]
