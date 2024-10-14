from warehouse.repository import ProductRepository, OrderRepository
from warehouse.schemas import ProductCreate, ProductUpdate, OrderCreate, OrderStatusUpdate
from warehouse.models import Product, OrderItem
from warehouse.exceptions import ProductNotFoundError, InsufficientStockError


class Service():
    def __init__(self, prod_rep:ProductRepository, ord_rep:OrderRepository):
        self._product_repository = prod_rep
        self._order_repository = ord_rep

    def create_product(self, product: ProductCreate):
        return self._product_repository.add_product(product)

    def get_products(self):
        return self._product_repository.get_products_list()

    def get_product_info(self, id: int):
        return self._product_repository.get_product_by_id(id)

    def update_product(self, id:int, product_data:ProductUpdate):
        return self._product_repository.update_product(id, product_data)

    def delete_product(self, id:int):
        return self._product_repository.delete_product(id)

    def make_order(self, order:OrderCreate):
        product_ids_from_order = [item.product_id for item in order.items]
        products_that_matches_ids = self._order_repository._session.query(Product).filter(Product.id.in_(product_ids_from_order)).all()
        products_dict = {product.id: product for product in products_that_matches_ids}

        order_items = []
        for item in order.items:
            product = products_dict.get(item.product_id)
            if product is None:
                raise ProductNotFoundError(item.product_id)
            if product.stock < item.amount:
                raise InsufficientStockError(product.id, product.stock, item.amount)
            product.stock -= item.amount
            order_items.append(OrderItem(product_id=item.product_id, amount=item.amount))
        return self._order_repository.create_order(order_items)

    def see_orders(self):
        return self._order_repository.get_orders()

    def get_special_order(self, id:int):
        self._order_repository.get_order_by_id(id)

    def update_status(self, id:int, status:OrderStatusUpdate):
        self._order_repository.update_order_status(id, status)


        
    



