# mypy: ignore-errors

from warehouse.database import get_db
from warehouse.models import Order, OrderItem, Product
from warehouse.schemas import OrderStatusUpdate


class OrderRepository:
    def __init__(self, session: get_db):
        self._session = session

    def create_order(self, order_items: list[OrderItem]) -> Order:
        db_order = Order()
        self._session.add(db_order)
        self._session.commit()
        self._session.refresh(db_order)

        for order_item in order_items:
            order_item.order_id = db_order.id
            self._session.add(order_item)

        self._session.commit()
        return db_order

    def get_orders(self, limit: int, offset: int) -> list[Order]:
        return self._session.query(Order).limit(limit).offset(offset).all()

    def get_order_by_id(self, id: int) -> Order:
        return self._session.query(Order).filter(Order.id == id).first()

    def update_order_status(self, id: int, status: OrderStatusUpdate) -> dict:
        order_for_update = self._session.query(Order).filter(Order.id == id).first()

        order_for_update.status = status.status
        self._session.commit()
        self._session.refresh(order_for_update)
        return {"status": status.status}
