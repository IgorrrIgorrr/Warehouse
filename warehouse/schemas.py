from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime


class ProductCreate(BaseModel):
    name:str 
    description:str | None 
    price:float 
    stock:int

class ProductReturn(BaseModel):
    id:int
    name:str 
    description:str | None 
    price:float 
    stock:int


    class Config:
        from_attributes = True


class ProductUpdate(BaseModel):
    name:str | None = None
    description:str | None = None 
    price:float | None = None
    stock:int | None = None


class OrderItemBase(BaseModel):
    product_id: int
    amount: int


class OrderCreate(BaseModel):
    items: List[OrderItemBase]


class OrderItemReturn(OrderItemBase):
    id:int


class OrderReturn(BaseModel):
    id: int
    created_at: datetime
    status: str
    order_items: List[OrderItemReturn]

    class Config:
        from_attributes = True


class OrderStatusUpdate(BaseModel):
    status: str

