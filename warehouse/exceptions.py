class ProductNotFoundError(Exception):
    def __init__(self, product_id):
        self.product_id = product_id
        super().__init__(f"Product with id {product_id} not found.")


class InsufficientStockError(Exception):
    def __init__(self, product_id, available, requested):
        self.product_id = product_id
        self.available = available
        self.requested = requested
        super().__init__(
            f"Not enough stock for product with id {product_id}. Available: {available}, requested: {requested}."
        )
