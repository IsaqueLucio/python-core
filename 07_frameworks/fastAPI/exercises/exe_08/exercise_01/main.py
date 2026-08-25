"""
See INSTRUCTIONS.md for the full task description.
"""

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import models
from database import Base, engine, get_db
from schemas import ProductCreate, ProductOut

# TODO: create all tables (Base.metadata.create_all(bind=engine))
Base.metadata.create_all(bind=engine)

# TODO: create the FastAPI app instance
app = FastAPI()

# TODO: POST "/products" endpoint, response_model=ProductOut
# receive ProductCreate, create a models.Product, add/commit/refresh, return it
@app.post("/products", response_model=ProductOut)
def post_products(product: ProductCreate, db: Session = Depends(get_db)):
    new_product = models.Product(**product.model_dump())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

# TODO: GET "/products" endpoint, response_model=list[ProductOut]
# return db.query(models.Product).all()
@app.get("/products", response_model=list[ProductOut])
def get_all_products(db: Session = Depends(get_db)):
    return db.query(models.Product).all()

# TODO: GET "/products/{product_id}" endpoint, response_model=ProductOut
# find by id, raise HTTPException(404, "Product not found") if missing
@app.get("/products/{product_id}", response_model=ProductOut)
def get_product(product_id: int, db: Session =  Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found.")
    return product
