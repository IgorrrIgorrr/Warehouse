from typing import Annotated
from fastapi import Depends, HTTPException, Security
from sqlalchemy.orm import Session
from warehouse.database import get_db
from warehouse.repositories.repository_products import ProductRepository
from warehouse.repositories.repository_orders import OrderRepository
from warehouse.service import Service
from fastapi.security.api_key import APIKeyHeader
from starlette.status import HTTP_403_FORBIDDEN
from warehouse.config import settings

API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

API_KEY = settings.API_KEY

async def get_api_key(api_key: str = Depends(api_key_header)):
    if api_key == API_KEY: 
        return api_key
    else:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="Could not validate API key",
        )



def get_product_repository(db:Annotated[Session, Depends(get_db)]) -> ProductRepository:
    return ProductRepository(db)

def get_order_repository(db:Annotated[Session, Depends(get_db)]) -> OrderRepository:
    return OrderRepository(db)


def get_service(prod_rep:Annotated[ProductRepository, Depends(get_product_repository)], ord_rep:Annotated[OrderRepository, Depends(get_order_repository)]) -> Service:
    return Service(prod_rep, ord_rep)


