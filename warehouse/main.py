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
from warehouse.exceptions import ProductNotFoundError, InsufficientStockError
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


@app.get("/products/{id}", response_model=ProductReturn)  # TODO добавить ошибку, если нету продукта
def get_product_by_id(id:int, service:Annotated[Service, Depends(get_service)]):
    return service.get_product_info(id)
   

@app.put("/products/{id}", response_model=ProductReturn) # TODO добавить ошибку, если нету продукта
def update_product(id:int, product_update: ProductUpdate, service:Annotated[Service, Depends(get_service)]):
    return service.update_product(id, product_update)


@app.delete("/products/{id}")
def delete_product(id:int, service:Annotated[Service, Depends(get_service)]):
    return service.delete_product(id)


@app.post("/orders", response_model=OrderReturn)
def create_order(order: OrderCreate, service:Annotated[Service, Depends(get_service)]):
    try:
        reslut = service.make_order(order) 
        return reslut
    except ProductNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except InsufficientStockError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred.") 

@app.get("/orders", response_model= List[OrderReturn])
def get_orders(service:Annotated[Service, Depends(get_service)]):
    return service.see_orders()


@app.get("/orders/{id}", response_model=OrderReturn)
def get_order_by_id(id:int, service:Annotated[Service, Depends(get_service)]):
    return service.get_special_order(id)


@app.patch("/orders/{id}/status")
def update_order_status(id:int, status: OrderStatusUpdate, service:Annotated[Service, Depends(get_service)]):
    return service.update_status(id, status)

