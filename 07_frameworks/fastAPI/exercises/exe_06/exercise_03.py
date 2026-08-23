"""
Exercise 3: Chained dependencies + a class-based dependency

Goal:
    Practice two more advanced (but common) patterns:
    - a dependency that depends on ANOTHER dependency (chaining)
    - using a class as a dependency instead of a function (useful when
      the dependency needs to bundle multiple related values, similar
      to injecting a configuration object)

Instructions:
    1. Create the FastAPI app instance.
    2. Create a dependency function `verify_token(x_token: str = Header(...))`
       that:
       - raises HTTPException(401, "Invalid token") if x_token != "abc123"
       - otherwise returns a dict like {"user": "isaque", "role": "admin"}

    3. Create a SECOND dependency function `require_admin(current_user: dict = Depends(verify_token))`
       that:
       - CHAINS on top of verify_token (notice the Depends() inside its
         own parameters -- this means FastAPI will run verify_token
         first, then pass its result here)
       - raises HTTPException(403, "Admin access required") if
         current_user["role"] != "admin"
       - otherwise returns current_user

    4. Create a GET "/admin/dashboard" endpoint that uses
       Depends(require_admin) and returns
       {"message": f"Welcome, {current_user['user']}"}.

    5. Now practice a CLASS-based dependency. Define a class:

       class Pagination:
           def __init__(self, page: int = 1, page_size: int = 10):
               self.page = page
               self.page_size = page_size

       A class with __init__ can be used directly with Depends(Pagination)
       -- FastAPI treats __init__'s parameters the same way it treats a
       regular dependency function's parameters (they become query params).

    6. Create a module-level list called `logs` with at least 15 short
       string entries (e.g. [f"Log entry {i}" for i in range(1, 16)]).

    7. Create a GET "/logs" endpoint that:
       - uses Depends(Pagination) to receive a `Pagination` INSTANCE
         (not a dict this time -- access it as pagination.page,
         pagination.page_size)
       - returns the correct slice of `logs` for that page
         (hint: start = (page - 1) * page_size)

Run it with:
    uvicorn exercise_03:app --reload

Test in http://127.0.0.1:8000/docs:
    - GET /admin/dashboard with header X-Token: abc123 -> should work
    - GET /admin/dashboard with header X-Token: wrong   -> 401
    - GET /logs?page=2&page_size=5 -> should return entries 6-10
"""

from fastapi import Depends, FastAPI, Header, HTTPException

# TODO: create the FastAPI app instance
app = FastAPI(
    title="Learning FastAPI: Exercise 3 - Chained dependencies + a class-based dependency",
    description="""
        Practice two more advanced (but common) patterns:
         -  a dependency that depends on ANOTHER dependency (chaining)
         -  using a class as a dependency instead of a function (useful when
            the dependency needs to bundle multiple related values, similar
            to injecting a configuration object)
      """,
    version="0.1.0",
)

# TODO: define verify_token dependency function
# parameter: x_token (str, via Header(...))
# raises 401 if x_token != "abc123"
# otherwise returns {"user": "isaque", "role": "admin"}
def verify_token(x_token: str = Header(...)):
   if x_token != "abc123":
      raise HTTPException(status_code=401, detail="Invalid token.")
   return  {"user": "Arthur", "role": "admin"}

# TODO: define require_admin dependency function, chained on verify_token
# parameter: current_user (dict, via Depends(verify_token))
# raises 403 if current_user["role"] != "admin"
# otherwise returns current_user
def require_admin(current_user: dict = Depends(verify_token)):
   if current_user["role"] != "admin":
      raise HTTPException(status_code=403)
   return current_user

# TODO: GET "/admin/dashboard" endpoint using Depends(require_admin)
@app.get("/admin/dashboard")
def get_adm_dashboard(current_user: dict = Depends(require_admin)):
   return {"message": f"Welcome, {current_user['user']}"}

# TODO: define the Pagination class
# __init__ params: page (int = 1), page_size (int = 10)
class Pagination:
   def __init__(self, page: int = 1, page_size: int = 10):
      self.page = page
      self.page_size = page_size

# TODO: create the `logs` list with at least 15 entries
logs = [f"Log entry {i}" for i in range(1, 16)]

# TODO: GET "/logs" endpoint using Depends(Pagination)
# return the correct slice based on page and page_size
@app.get("/logs")
def get_logs(pagination: Pagination = Depends(Pagination)):
   start = (pagination.page - 1) * pagination.page_size
   end = start + pagination.page_size
   return logs[start:end]
