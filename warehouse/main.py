from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import Annotated, List, Optional
from warehouse.models import Base, Product, Order, OrderItem
from warehouse.database import engine, get_db
from warehouse.schemas import ProductCreate, ProductReturn, ProductUpdate, OrderCreate, OrderItemBase, OrderReturn, OrderStatusUpdate

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
    try:
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
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="An error occurred while updating the product")


@app.delete("/products/{id}")
def delete_product(id:int, db:Annotated[Session, Depends(get_db)]):
    try:
        product_data = db.query(Product).filter(Product.id == id).first()
        if product_data is None:
            raise HTTPException(status_code= 404, detail= "Product not found")
        db.delete(product_data)
        db.commit()
        return {"detail": "Product deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="An error occurred while deleting the product")



@app.post("/orders", response_model=OrderReturn)
def create_order(order: OrderCreate, db: Annotated[Session, Depends(get_db)]):
    try:
        order_items = []
        for item in order.items:
            product = db.query(Product).filter(Product.id == item.product_id).first()
            if product is None:
                raise HTTPException(status_code=404, detail=f"Product with id {item.product_id} not found")
            if product.stock < item.amount:
                raise HTTPException(status_code=400, detail=f"Not enough stock for product {item.product_id}")

            product.stock -= item.amount
            order_items.append(OrderItem(product_id=item.product_id, amount=item.amount))

        db_order = Order()  
        db.add(db_order)
        db.commit()
        db.refresh(db_order)

        for order_item in order_items:
            order_item.order_id = db_order.id  
            db.add(order_item)

        db.commit() 
        return db_order  

    except Exception as e:
        db.rollback() 
        raise HTTPException(status_code=500, detail=str(e))  
    



@app.get("/orders", response_model= List[OrderReturn])
def get_orders(db:Annotated[Session, Depends(get_db)]):
    orders = db.query(Order).all()
    return orders



@app.get("/orders/{id}", response_model=OrderReturn)
def get_order_by_id(id:int, db:Annotated[Session, Depends(get_db)]):
    order = db.query(Order).filter(Order.id == id).first()
    if order is None:
            raise HTTPException(status_code=404, detail=f"Order with id {id} not found")
    return order


@app.patch("/orders/{id}/status")
def update_order_status(id:int, status: OrderStatusUpdate, db:Annotated[Session, Depends(get_db)]):
        try:
            order = db.query(Order).filter(Order.id == id).first()
        
            if order is None:
                raise HTTPException(status_code=404, detail="Order not found")

            order.status = status.status
            db.commit()
            db.refresh(order)

            return {"order_id": order.id, "status": order.status}
        except Exception as e:
            db.rollback()  
            raise HTTPException(status_code=500, detail=str(e))

