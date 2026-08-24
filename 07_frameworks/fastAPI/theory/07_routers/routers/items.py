"""
All /items endpoints live here. Same pattern as users.py -- this is
the whole point: each domain is self-contained and easy to find.
"""

from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/items", tags=["items"])

items = [
    {"id": 1, "name": "Keyboard"},
    {"id": 2, "name": "Mouse"},
]


@router.get("")
def list_items():
    return items


@router.get("/{item_id}")
def get_item(item_id: int):
    for item in items:
        if item["id"] == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")
