from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import Annotated, List
from warehouse.models import Base, Product, Order, OrderItem
from warehouse.database import engine, get_db
from warehouse.schemas import ProductCreate, ProductReturn, ProductUpdate

app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.post("/products")
def create_product(product_data:ProductCreate, db:Annotated[Session, Depends(get_db)]):
    try:
        new_product = Product(name = product_data.name, description = product_data.description, price = product_data.price, stock = product_data.stock)
        db.add(new_product)
        db.commit()
        db.refresh(new_product)
        return new_product
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="An error occurred while creating the product")


@app.get("/products", response_model=List[ProductReturn])
def get_products(db:Annotated[Session, Depends(get_db)]):
    products = db.query(Product).all()
    if not products:
        raise HTTPException(status_code=404, detail="No products found")
    return products


@app.get("/products/{id}", response_model=ProductReturn)
def get_product_by_id(id:int, db:Annotated[Session, Depends(get_db)]):
    product_data = db.query(Product).filter(Product.id == id).first()
    if product_data is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product_data


@app.put("/products/{id}", response_model=ProductReturn)
def update_product(id:int, product_update: ProductUpdate, db:Annotated[Session, Depends(get_db)]):
    product_data = db.query(Product).filter(Product.id == id).first()
    
    if product_data is None:
        raise HTTPException(status_code=404, detail="Product not found")
    
    if product_update.name is not None:
        product_data.name = product_update.name
    if product_update.description is not None:
        product_data.description = product_update.description
    if product_update.price is not None:
        product_data.price = product_update.price
    if product_update.stock is not None:
        product_data.stock = product_update.stock
    
    db.commit()
    db.refresh(product_data)
    return product_data


@app.delete("/products/{id}")
def delete_product(db:Annotated[Session, Depends(get_db)]):
    product_data = db.query(Product).filter(Product.id == id).first()
    if product_data is None:
        raise HTTPException(status_code= 404, detail= "Product not found")
    db.delete(product_data)
    db.commit()
    return



@app.post("/orders")
def create_order(db:Annotated[Session, Depends(get_db)]):
    pass

@app.get("/orders")
def get_orders(db:Annotated[Session, Depends(get_db)]):
    pass

@app.get("/orders/{id}")
def get_order_by_id(db:Annotated[Session, Depends(get_db)]):
    pass


@app.patch("/orders/{id}/status")
def update_order_status(db:Annotated[Session, Depends(get_db)]):
    pass


