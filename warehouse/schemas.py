from pydantic import BaseModel

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
    name:str | None
    description:str | None 
    price:float | None
    stock:int | None

