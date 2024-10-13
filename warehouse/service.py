from warehouse.repository import ProductRepository, OrderRepository
from warehouse.schemas import ProductCreate, ProductUpdate, OrderCreate, OrderStatusUpdate

class Service():
    def __init__(self, prod_rep:ProductRepository, ord_rep:OrderRepository):
        self._product_repository = prod_rep
        self._order_repository = ord_rep

    def create_product(self, product: ProductCreate):
        self._product_repository.add_product(product)

    def get_products(self):
        self._product_repository.get_products_list

    def get_product_info(self, id: int):
        self._product_repository.get_product_by_id(id)

    def update_product(self, id:int, product_data:ProductUpdate):
        self._product_repository.update_product(id, product_data)

    def delete_product(self, id:int):
        self._product_repository.delete_product(id)

    def make_order(self, order:OrderCreate):
        self._order_repository.create_order(order)

    def see_orders(self):
        self._order_repository.get_orders()

    def get_special_order(self, id:int):
        self._order_repository.get_order_by_id(id)

    def update_status(self, id:int, status:OrderStatusUpdate):
        self._order_repository.update_order_status(id, status)


        
    



