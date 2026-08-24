"""
See INSTRUCTIONS.md for the full task description.

This file holds dependencies SHARED across multiple routers -- a
common pattern in real projects, where dependencies.py (or a
dependencies/ package, for bigger apps) sits alongside routers/ and
main.py.
"""

from fastapi import Header

# TODO: define get_current_user dependency function
# parameter: x_user (str, via Header(...))
# returns {"username": x_user}
def get_current_user(x_user: str = Header(...)):
    return {"username": x_user}