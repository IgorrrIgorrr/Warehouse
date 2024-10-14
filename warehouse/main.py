from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import Annotated, List, Optional
from warehouse.models import Base, Product, Order, OrderItem
from warehouse.database import engine, get_db
from warehouse.schemas import ProductCreate, ProductReturn, ProductUpdate, OrderCreate, OrderItemBase, OrderReturn, OrderStatusUpdate
from warehouse import crud
from warehouse.repository import ProductRepository, OrderRepository
from warehouse.service import Service
from typing import Annotated



app = FastAPI()

Base.metadata.create_all(bind=engine)


def get_product_repository(db:Annotated[Session, Depends(get_db)]) -> ProductRepository:
    return ProductRepository(db)

def get_order_repository(db:Annotated[Session, Depends(get_db)]) -> OrderRepository:
    return OrderRepository(db)


def get_service(prod_rep:Annotated[ProductRepository, Depends(get_product_repository)], ord_rep:Annotated[OrderRepository, Depends(get_order_repository)]) -> Service:
    return Service(prod_rep, ord_rep)



@app.post("/products")
def create_product(product_data:ProductCreate, service:Annotated[Service, Depends(get_service)]):
    return service.create_product(product_data)   


@app.get("/products", response_model=List[ProductReturn])
def get_products(service:Annotated[Service, Depends(get_service)]):   
    return service.get_products()


@app.get("/products/{id}", response_model=ProductReturn)
def get_product_by_id(id:int, service:Annotated[Service, Depends(get_service)]):
    return service.get_product_info(id)
   

@app.put("/products/{id}", response_model=ProductReturn)
def update_product(id:int, product_update: ProductUpdate, service:Annotated[Service, Depends(get_service)]):
    return service.update_product(id, product_update)


@app.delete("/products/{id}")
def delete_product(id:int, service:Annotated[Service, Depends(get_service)]):
    return service.delete_product(id)







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

