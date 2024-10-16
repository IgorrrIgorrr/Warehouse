from datetime import datetime

from pydantic import BaseModel


class ProductCreate(BaseModel):
    name: str
    description: str | None
    price: float
    stock: int


class ProductReturn(BaseModel):
    id: int
    name: str
    description: str | None
    price: float
    stock: int

    class Config:
        from_attributes = True


class ProductUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    stock: int | None = None


class OrderItemBase(BaseModel):
    product_id: int
    amount: int


class OrderItemReturn(OrderItemBase):
    id: int


class OrderReturn(BaseModel):
    id: int
    created_at: datetime
    status: str
    order_items: list[OrderItemReturn]

    class Config:
        from_attributes = True


class OrderCreate(BaseModel):
    items: list[OrderItemBase]


class OrderStatusUpdate(BaseModel):
    status: str
