from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session
from warehouse.database import get_db
from warehouse.repositories.repository_products import ProductRepository
from warehouse.repositories.repository_orders import OrderRepository
from warehouse.service import Service

def get_product_repository(db:Annotated[Session, Depends(get_db)]) -> ProductRepository:
    return ProductRepository(db)

def get_order_repository(db:Annotated[Session, Depends(get_db)]) -> OrderRepository:
    return OrderRepository(db)


def get_service(prod_rep:Annotated[ProductRepository, Depends(get_product_repository)], ord_rep:Annotated[OrderRepository, Depends(get_order_repository)]) -> Service:
    return Service(prod_rep, ord_rep)


