from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import Annotated, List, Optional
from warehouse.models import Base, Product, Order, OrderItem
from warehouse.database import engine, get_db
from warehouse.schemas import ProductCreate, ProductReturn, ProductUpdate, OrderCreate, OrderItemBase, OrderReturn, OrderStatusUpdate
from warehouse.exceptions import DatabaseError



def create_product_in_db(product_data:ProductCreate, db:Session):
    new_product = Product(name = product_data.name, description = product_data.description, price = product_data.price, stock = product_data.stock)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


    
    
def get_products_from_db(db:Session):
    products = db.query(Product).all()
    if not products:
        raise HTTPException(status_code=404, detail="No products found")
    return products    

def get_product_by_id(id:int, db:Session):
    product_data = db.query(Product).filter(Product.id == id).first()
    if product_data is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product_data




