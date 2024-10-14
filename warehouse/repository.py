from warehouse.database import get_db
from warehouse.models import Product, Order, OrderItem 
from warehouse.schemas import ProductCreate, ProductUpdate, OrderCreate, OrderStatusUpdate
from typing import List

class ProductRepository():
    def __init__(self, session: get_db):
        self._session = session
    
    def add_product(self, product_data: ProductCreate):
        new_product = Product(name = product_data.name, description = product_data.description, price = product_data.price, stock = product_data.stock)
        self._session.add(new_product)
        self._session.commit()
        self._session.refresh(new_product)
        return new_product

    def get_products_list(self):
        return self._session.query(Product).all() # обработать пустоту в сервисе

    def get_product_by_id(self, id: int):
        return self._session.query(Product).filter(Product.id == id).first() # если не будет обработать

    def update_product(self, id:int, product_new_data: ProductUpdate):
        product_updated = self._session.query(Product).filter(Product.id == id).first()

        if product_new_data.name is not None:
            product_updated.name = product_new_data.name

        if product_new_data.description is not None:
            product_updated.description = product_new_data.description

        if product_new_data.price is not None:
            product_updated.price = product_new_data.price

        if product_new_data.stock is not None:
            product_updated.stock = product_new_data.stock
         
        self._session.commit()
        self._session.refresh(product_updated)
        return product_updated
    
    def delete_product(self, id:int):
        product_for_deletion = self._session.query(Product).filter(Product.id == id).first()
        self._session.delete(product_for_deletion)
        self._session.commit()
        return {"reply":f"product with id {id} was deleted"}
       

class OrderRepository():
    def __init__(self, session: get_db):
        self._session = session

    def create_order(self, order_items:List[OrderItem]): #тут!!!!!!!!!!!!!!!!!
        db_order = Order()  
        self._session.add(db_order)
        self._session.commit()
        self._session.refresh(db_order)

        for order_item in order_items:
            order_item.order_id = db_order.id  
            self._session.add(order_item)
        
        self._session.commit()
        return db_order


    def get_orders(self):
        return self._session.query(Order).all()
    
    def get_order_by_id(self, id:int):
        return self._session.query(Order).filter(Order.id == id).first()
    
    def update_order_status(self, id:int, status:OrderStatusUpdate):
        order_for_update = self._session.query(Order).filter(Order.id == id).first()
        order_for_update.status = status.status
        self._session.commit()
        self._session.refresh(order_for_update)
        return {"new status":f"{status.status}"}








    

        