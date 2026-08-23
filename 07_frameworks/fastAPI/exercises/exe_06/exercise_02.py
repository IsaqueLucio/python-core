"""
Exercise 2: A dependency that validates and raises errors

Goal:
    Practice a dependency that does more than just collect params --
    it actively validates something and can short-circuit the request
    with HTTPException, similar to an auth guard.

Instructions:
    1. Create the FastAPI app instance.
    2. Create a module-level list called `orders` with at least 4
       dicts, each with "id" (int) and "total" (float).
    3. Create a dependency function `get_order_or_404(order_id: int)`
       that:
       - searches `orders` for a matching "id"
       - returns the matching order dict if found
       - raises HTTPException(404, "Order not found") if not found

       Note: order_id here comes from the PATH, but dependencies can
       read path params too -- FastAPI matches the dependency's
       parameter name ("order_id") to the path param of whatever
       endpoint uses it.
    4. Create a GET "/orders/{order_id}" endpoint that:
       - uses Depends(get_order_or_404)
       - simply returns the order it received (the dependency already
         did the lookup and error handling)
    5. Create a GET "/orders/{order_id}/summary" endpoint that:
       - ALSO uses Depends(get_order_or_404) (reusing the same lookup)
       - returns {"order_id": ..., "total_with_tax": total * 1.1}

Run it with:
    uvicorn exercise_02:app --reload

Test in http://127.0.0.1:8000/docs:
    - GET /orders/1              -> should work
    - GET /orders/999            -> 404 Order not found
    - GET /orders/1/summary       -> should work, showing total_with_tax
    - GET /orders/999/summary     -> 404 Order not found (same dependency
                                       protects both endpoints)
"""

from fastapi import Depends, FastAPI, HTTPException

# TODO: create the FastAPI app instance
app = FastAPI(
    title="Learning FastAPI: Exercise 2 - A dependency that validates and raises errors",
    description="""
        Practice a dependency that does more than just collect params --
        it actively validates something and can short-circuit the request
        with HTTPException, similar to an auth guard.
      """,
    version="0.1.0",
)

# TODO: create the `orders` list with at least 4 sample orders
# each with "id", "total"
orders = [
    {"id": 1, "total": 150.00},
    {"id": 2, "total": 320.50},
    {"id": 3, "total": 89.90},
    {"id": 4, "total": 450.00},
]

# TODO: define the get_order_or_404 dependency function
# parameter: order_id (int)
# returns the matching order, or raises HTTPException(404, "Order not found")
def get_order_or_404(order_id: int):
    for order in orders:
        if order_id == order["id"]:
            return order
    raise HTTPException (status_code=404, detail="Order not found.")

# TODO: GET "/orders/{order_id}" endpoint using Depends(get_order_or_404)
@app.get("/orders/{order_id}")
def get_order_by_id(order: dict = Depends(get_order_or_404)):
    return order

# TODO: GET "/orders/{order_id}/summary" endpoint using
# Depends(get_order_or_404)
@app.get("/orders/{order_id}/summary")
def get_order_summary(order: dict = Depends(get_order_or_404)):
    order_id = order["id"]
    total_with_tax = order["total"] * 1.1
    return {
        "order_id": order_id,
        "total_with_tax": total_with_tax
        }
