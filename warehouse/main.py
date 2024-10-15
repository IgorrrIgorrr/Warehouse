from fastapi import FastAPI, Depends, HTTPException, Query
from typing import Annotated
from warehouse.models import Base, Product, Order
from warehouse.database import engine, get_db
from warehouse.schemas import ProductCreate, ProductReturn, ProductUpdate, OrderCreate, OrderReturn, OrderStatusUpdate
from warehouse.service import Service
from warehouse.exceptions import ProductNotFoundError, InsufficientStockError
from typing import Annotated
from warehouse.dependencies import get_service


app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.post("/products", response_model = ProductReturn)
def create_product(product_data:ProductCreate, service:Annotated[Service, Depends(get_service)]) -> Product:
    return service.create_product(product_data)   


@app.get("/products", response_model=list[ProductReturn])     
def get_products(service:Annotated[Service, Depends(get_service)],page: int = Query(1, ge=1), limit: int = Query(10, ge=1)) -> list[Product]:   
    return service.get_products(page, limit)


@app.get("/products/{id}", response_model=ProductReturn)  # TODO добавить ошибку, если нету продукта
def get_product_by_id(id:int, service:Annotated[Service, Depends(get_service)]) -> Product:
    return service.get_product_info(id)
   

@app.put("/products/{id}", response_model=ProductReturn) # TODO добавить ошибку, если нету продукта
def update_product(id:int, product_update: ProductUpdate, service:Annotated[Service, Depends(get_service)]) -> Product:
    return service.update_product(id, product_update)


@app.delete("/products/{id}")
def delete_product(id:int, service:Annotated[Service, Depends(get_service)]) -> dict:
    return service.delete_product(id)


@app.post("/orders", response_model=OrderReturn)
def create_order(order: OrderCreate, service:Annotated[Service, Depends(get_service)]) -> Order:
    try:
        result = service.make_order(order) 
    except ProductNotFoundError as e:
        raise HTTPException(status_code=404, detail="No products found")
    except InsufficientStockError as e:
        raise HTTPException(status_code=400, detail="Not enough stock to make order")
    else:
        return result

@app.get("/orders", response_model= list[OrderReturn])
def get_orders(service:Annotated[Service, Depends(get_service)],page: int = Query(1, ge=1), limit: int = Query(10, ge=1)):
    return service.list_orders(page, limit)


@app.get("/orders/{id}", response_model=OrderReturn)
def get_order_by_id(id:int, service:Annotated[Service, Depends(get_service)]):
    return service.get_special_order(id)


@app.patch("/orders/{id}/status")
def update_order_status(id:int, status: OrderStatusUpdate, service:Annotated[Service, Depends(get_service)]) -> dict:
    return service.update_status(id, status)

