from warehouse.database import get_db
from warehouse.models import Product, Order, OrderItem 
from warehouse.schemas import ProductCreate, ProductUpdate, OrderCreate, OrderStatusUpdate

class ProductRepository():
    def __init__(self, session: get_db):
        self._session = session
    
    def add_product(self, product_data: ProductCreate) -> Product:
        new_product = Product(name = product_data.name, description = product_data.description, price = product_data.price, stock = product_data.stock)
        self._session.add(new_product)
        self._session.commit()
        self._session.refresh(new_product)
        return new_product

    def get_products_list(self, limit: int, offset: int) -> list[Product]:
        return self._session.query(Product).limit(limit).offset(offset).all() 

    def get_product_by_id(self, id: int) -> Product:
        return self._session.query(Product).filter(Product.id == id).first() 

    def update_product(self, id:int, product_new_data: ProductUpdate) -> Product:
        product_updated = self._session.query(Product).filter(Product.id == id).first()
        update_fields = {
        'name': product_new_data.name,
        'description': product_new_data.description,
        'price': product_new_data.price, 
        'stock': product_new_data.stock
        }       
            
        for field, value in update_fields.items():
            if value is not None:
                setattr(product_updated, field, value)

         
        self._session.commit()
        return product_updated
    
    def delete_product(self, id:int) -> dict:
        product_for_deletion = self._session.query(Product).filter(Product.id == id).first()
        self._session.delete(product_for_deletion)
        self._session.commit()
        return {"reply":f"product with id {id} was deleted"}
       










    

        