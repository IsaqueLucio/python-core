"""
See ../INSTRUCTIONS.md for the full task description.
"""

from fastapi import APIRouter, Depends, Header, HTTPException

# TODO: define verify_admin_key dependency function
# parameter: x_admin_key (str, via Header(...))
# raises 401 if x_admin_key != "letmein"
def verify_admin_key(x_admin_key: str = Header(...)):
    if x_admin_key != "letmein":
        raise HTTPException(status_code=401, detail="Invalid token.")

# TODO: create the router with prefix="/admin", tags=["admin"],
# and dependencies=[Depends(verify_admin_key)]
router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(verify_admin_key)]
)

# TODO: create the `logs` list with at least 5 entries
logs = [
    "User logged in",
    "Book borrowed",
    "Book returned",
    "User logged out",
    "System backup completed",
]

# TODO: GET "/logs" endpoint (becomes /admin/logs) returning the list
# (no Depends needed here -- the router already protects it)
@router.get("/logs")
def get_logs():
    return logs

# TODO: DELETE "/logs" endpoint (becomes /admin/logs) clearing the list
# and returning {"message": "Logs cleared"}
@router.delete("/logs")
def delete_logs():
    logs.clear()
    return {"message": "Logs cleared"}