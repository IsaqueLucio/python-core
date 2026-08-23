"""
Exercise 1: A reusable filtering dependency

Goal:
    Practice extracting shared query-param logic into a dependency
    function and reusing it across two endpoints.

Instructions:
    1. Create the FastAPI app instance.
    2. Create a module-level list called `products` with at least 6
       dicts, each with "id" (int), "name" (str), "category" (str),
       and "price" (float). Include at least two different categories.
    3. Create a dependency function `category_filter(category: str | None = None)`
       that simply returns {"category": category}.
    4. Create a GET "/products" endpoint that:
       - uses Depends(category_filter)
       - if category is None, returns all products
       - otherwise, returns only products matching that category
    5. Create a GET "/products/count" endpoint that:
       - ALSO uses Depends(category_filter) (reusing the same dependency)
       - returns {"total": <count>}, counting only matching products
         (or all products if category is None)

Run it with:
    uvicorn exercise_01:app --reload

Test in http://127.0.0.1:8000/docs:
    - GET /products                     -> all products
    - GET /products?category=Electronics -> filtered list
    - GET /products/count?category=Electronics -> {"total": <n>}
"""

from fastapi import Depends, FastAPI

# TODO: create the FastAPI app instance
app = FastAPI(
    title="Learning FastAPI: Exercise 1 - A reusable filtering dependency",
    description="Practice extracting shared query-param logic into a dependency function and reusing it across two endpoints.",
    version="0.1.0",
)

# TODO: create the `products` list with at least 6 sample products
# each with "id", "name", "category", "price"
products = [
    {"id": 1, "name": "Notebook", "category": "Eletrônicos", "price": 3500.00},
    {"id": 2, "name": "Smartphone", "category": "Eletrônicos", "price": 2200.00},
    {"id": 3, "name": "Fone de ouvido", "category": "Acessórios", "price": 350.00},
    {"id": 4, "name": "Teclado", "category": "Acessórios", "price": 250.00},
    {"id": 5, "name": "Mouse", "category": "Acessórios", "price": 120.00},
    {"id": 6, "name": "Monitor", "category": "Eletrônicos", "price": 1500.00},
]

# TODO: define the category_filter dependency function
# parameter: category (str | None = None)
# returns {"category": category}
def category_filter(category: str | None = None):
    return {"category": category}

# TODO: GET "/products" endpoint using Depends(category_filter)
@app.get("/products")
def get_products(category: dict = Depends(category_filter)):
    if category["category"] == None:
        return products
    temp = []
    for product in products:
        if product["category"] == category["category"]:
            temp.append(product)
    if not temp:
        return f"Category {category['category']} not found."
    return temp   

# TODO: GET "/products/count" endpoint using Depends(category_filter)
@app.get("/products/count")
def get_products_count(category: dict = Depends(category_filter)):
    if category["category"] == None:
        return {}
    temp = []
    for product in products:
        if product["category"] == category["category"]:
            temp.append(product)
    if not temp:
        return f"Category {category['category']} not found."
    return {"category": category['category'],
            "total_products": len(temp)}
