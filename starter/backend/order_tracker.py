# This module contains the OrderTracker class, which encapsulates the core
# business logic for managing orders.

class OrderTracker:
    """
    Manages customer orders, providing functionalities to add, update,
    and retrieve order information.
    """
    def __init__(self, storage):
        required_methods = ['save_order', 'get_order', 'get_all_orders']
        for method in required_methods:
            if not hasattr(storage, method) or not callable(getattr(storage, method)):
                raise TypeError(f"Storage object must implement a callable '{method}' method.")
        self.storage = storage

    def add_order(self, order_id: str, item_name: str, quantity: int, customer_id: str, status: str = "pending"):
        if self.storage.get_order(order_id):
            raise ValueError(f"Order with ID '{order_id}' already exists.")

        order = {
            "order_id": order_id,
            "item_name": item_name,
            "quantity": quantity,
            "customer_id": customer_id,
            "status": status
        }

        self.storage.save_order(order_id, order)
        return order

    def get_order_by_id(self, order_id: str):
        if not isinstance(order_id, str) or not order_id.strip():
            raise ValueError("Order ID cannot be empty.")

        return self.storage.get_order(order_id)

    def update_order_status(self, order_id: str, new_status: str):
        valid_statuses = {
            "pending",
            "processing",
            "shipped",
            "delivered",
            "cancelled"
        }

        if new_status not in valid_statuses:
            raise ValueError(f"Invalid status: '{new_status}'.")

        if not isinstance(order_id, str) or not order_id.strip():
            raise ValueError("Order ID cannot be empty.")

        order = self.storage.get_order(order_id)

        if order is None:
            raise ValueError(f"Order with ID '{order_id}' does not exist.")

        updated_order = order.copy()
        updated_order["status"] = new_status

        self.storage.save_order(order_id, updated_order)

        return updated_order

    def list_all_orders(self):
        orders = self.storage.get_all_orders()
        return list(orders.values())
    def list_orders_by_status(self, status: str):
        valid_statuses = {
            "pending",
            "processing",
            "shipped",
            "delivered",
            "cancelled"
        }

        if not isinstance(status, str) or not status.strip():
            raise ValueError("Status cannot be empty.")

        if status not in valid_statuses:
            raise ValueError(f"Invalid status: '{status}'.")

        orders = self.storage.get_all_orders()

        return [
            order
            for order in orders.values()
            if order.get("status") == status
        ]