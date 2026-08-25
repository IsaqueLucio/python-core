# Exercise 1: Basic CRUD with SQLAlchemy (Create + Read)

## Goal
Practice the exact same pattern from the theory files (database.py,
models.py, schemas.py, main.py), but for a new entity: Product.

## Structure to build

    exercise_01/
    ├── database.py   (copy the theory database.py -- it's fully generic,
    │                  nothing there is specific to "books")
    ├── models.py
    ├── schemas.py
    └── main.py

`database.py` already has everything filled in for you (it's the same
in every exercise of this topic -- copy it as-is from
theory/08_database/database.py). `models.py`, `schemas.py` and
`main.py` have TODOs for you to fill in.

## Instructions

1. In `models.py`:
   - Define `class Product(Base):` with `__tablename__ = "products"`
   - Columns: id (Integer, primary_key, index), name (String,
     nullable=False), price (Float, nullable=False),
     quantity (Integer, default=0)

2. In `schemas.py`:
   - Define `ProductCreate` (input): name (str), price (float),
     quantity (int = 0)
   - Define `ProductOut` (output): id (int), name (str), price (float),
     quantity (int), with `model_config = ConfigDict(from_attributes=True)`

3. In `main.py`:
   - Call `Base.metadata.create_all(bind=engine)` at module level
     (before defining the app's endpoints, same as the theory example)
   - Create the FastAPI app instance
   - `POST "/products"` with response_model=ProductOut: receives a
     ProductCreate, creates a `models.Product`, adds/commits/refreshes
     it, returns it
   - `GET "/products"` with response_model=list[ProductOut]: returns
     `db.query(models.Product).all()`
   - `GET "/products/{product_id}"` with response_model=ProductOut:
     finds by id, raises HTTPException(404, "Product not found") if
     missing

## Run it

From INSIDE the `exercise_01/` folder:

    uvicorn main:app --reload

A file `app.db` will be created automatically. Delete it any time to
reset your data.

## Test in http://127.0.0.1:8000/docs

    POST /products
    Body: {"name": "Keyboard", "price": 250.0, "quantity": 5}
    -> should return it with an "id"

    GET /products
    -> should return the list, including what you just created

    GET /products/1
    -> should return that single product

    GET /products/999
    -> 404 Product not found
