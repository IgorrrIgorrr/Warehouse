from pydantic import BaseModel
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
        orm_mode = True


class ProductUpdate(BaseModel):
    name:None | None
    description:str | None 
    price:float | None
    stock:int | None







class OrderItemBase(BaseModel):
    product_id: int
    quantity: int


class OrderCreate(BaseModel):
    items: List[OrderItemBase]


class OrderItemReturn(OrderItemBase):
    id:int


class OrderReturn(BaseModel):
    id: int
    created_at: datetime
    status: str
    items: List[OrderItemReturn]

    class Config:
        orm_mode = True


class OrderStatusUpdate(BaseModel):
    status: str

