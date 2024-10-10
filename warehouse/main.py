from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import Annotated
from warehouse.models import Base, Product, Order, OrderItem
from warehouse.database import engine, get_db

app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.post("/products")
def create_product(name:str, description:str, price:float, stock: int, db:Annotated[Session, Depends(get_db)]):
    product = Product(name=name, description = description, price = price, stock = stock)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


@app.get("/products")
def get_products(db:Annotated[Session, Depends(get_db)]):
    pass

@app.get("/products/{id}")
def get_product_by_id(db:Annotated[Session, Depends(get_db)]):
    pass

@app.put("/products/{id}")
def update_product(db:Annotated[Session, Depends(get_db)]):
    pass

@app.delete("/products/{id}")
def delete_product(db:Annotated[Session, Depends(get_db)]):
    pass




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


