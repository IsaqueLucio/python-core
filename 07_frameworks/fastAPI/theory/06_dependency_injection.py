"""
Topic: Dependency Injection with Depends()

So far, every endpoint has been self-contained: all its logic lives
inside the function body. But real APIs have cross-cutting concerns
that repeat across MANY endpoints: reading a pagination query param,
checking an API key, getting a database session, verifying a logged-in
user, etc. Copy-pasting that logic into every function is a maintenance
nightmare.

`Depends()` lets you extract reusable logic into its own function and
"inject" its return value into any endpoint that needs it.

Coming from Spring Boot, think of it this way:
- Depends()          -> conceptually similar to Spring's Dependency
                         Injection (@Autowired, constructor injection),
                         but explicit and per-parameter instead of
                         class-wide and annotation-driven.
- A dependency function -> similar to a @Bean or a @Component you'd
                            inject, except in FastAPI it's just a
                            plain Python function (or callable class).
- Dependencies can depend on OTHER dependencies, forming a chain,
  similar to how Spring beans can depend on other beans.

How to run this file:
    uvicorn theory.06_dependency_injection:app --reload
"""

from fastapi import Depends, FastAPI, HTTPException, Header

app = FastAPI(
    title="Learning FastAPI",
    description="Dependency injection with Depends()",
    version="0.1.0",
)

# --- A simple dependency: shared pagination logic ---
# This is just a normal function. Its parameters become query params
# automatically (same rules as regular endpoint functions).
def pagination_params(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}

items = [{"id": i, "name": f"Item {i}"} for i in range(1, 51)]

# Depends(pagination_params) tells FastAPI: "before running this
# endpoint, call pagination_params() (reading skip/limit from the
# query string) and inject its return value here."
@app.get("/items")
def list_items(pagination: dict = Depends(pagination_params)):
    """
    Example: GET /items?skip=10&limit=5

    Without Depends, you'd have to repeat `skip: int = 0, limit: int = 10`
    as parameters on EVERY endpoint that needs pagination. With
    Depends, you write it once and reuse it everywhere.
    """
    start = pagination["skip"]
    end = start + pagination["limit"]
    return items[start:end]

@app.get("/items/reversed")
def list_items_reversed(pagination: dict = Depends(pagination_params)):
    # Same dependency, reused in a second endpoint with zero repetition.
    start = pagination["skip"]
    end = start + pagination["limit"]
    return list(reversed(items))[start:end]

# --- A dependency that can raise errors: simple auth check ---
# Dependencies can use HTTPException just like regular endpoints.
# This is the closest FastAPI equivalent to a Spring Security filter
# or an @PreAuthorize check, just much more minimal.
def verify_api_key(x_api_key: str = Header(...)):
    """
    Header(...) reads a value from the request HEADERS, not the query
    string or body. Here we expect a header literally named "X-API-Key".
    """
    if x_api_key != "secret123":
        raise HTTPException(status_code=401, detail="Invalid API key")
    return x_api_key

@app.get("/admin/stats")
def admin_stats(api_key: str = Depends(verify_api_key)):
    """
    Because verify_api_key() raises HTTPException BEFORE this function
    body ever runs, this endpoint is effectively "protected" -- no
    need to write the auth check manually here.
    """
    return {"total_items": len(items), "authenticated_with": api_key}

# Key takeaways:
# 1. Depends(some_function) reuses logic across multiple endpoints,
#    without copy-pasting parameters or validation code.
# 2. A dependency is just a plain function; its own parameters follow
#    the exact same rules as endpoint parameters (path/query/body/header).
# 3. Dependencies can raise HTTPException to short-circuit the request
#    before the endpoint body runs -- perfect for auth-style checks.
# 4. This is the foundation for real authentication (JWT/OAuth2) and
#    for database session management, both coming up in later topics.