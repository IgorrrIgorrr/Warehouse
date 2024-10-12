from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import Annotated, List, Optional
from warehouse.models import Base, Product, Order, OrderItem
from warehouse.database import engine, get_db
from warehouse.schemas import ProductCreate, ProductReturn, ProductUpdate, OrderCreate, OrderItemBase, OrderReturn, OrderStatusUpdate
from warehouse.crud import 



def create_product(product_data:ProductCreate, db:Session):
    try:
        new_product = Product(name = product_data.name, description = product_data.description, price = product_data.price, stock = product_data.stock)
        db.add(new_product)
        db.commit()
        db.refresh(new_product)
        return new_product
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="An error occurred while creating the product")
    
def get_products(db:Session):
    products = db.query(Product).all()
    if not products:
        raise HTTPException(status_code=404, detail="No products found")
    return products    