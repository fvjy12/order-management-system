from enum import Enum
from datetime import datetime

class OrderStatus(Enum):
    NEW = "Новый"
    PROCESSING = "В обработке"
    SHIPPED = "Отправлен"
    DELIVERED = "Доставлен"
    CANCELLED = "Отменен"

class Order:
    def __init__(self, order_id, customer_name, product, quantity, price):
        self.order_id = order_id
        self.customer_name = customer_name
        self.product = product
        self.quantity = quantity
        self.price = price
        self.status = OrderStatus.NEW
        self.created_data = datetime.now()
        self.updated = datetime.now()
        self.notes = ""

    def update_status(self, new_status):
        self.status = new_status
        self.updated = datetime.now()

    def add_note(self, note):
        self.notes += f"[{datetime.now().strftime('%Y-%m-%d %H:%M')}] {note}\n"

    def get_total_price(self):
        return self.quantity * self.price

    def to_dict(self):
        return {
            "order_id": self.order_id,
            "customer_name" : self.customer_name,
            "product" : self.product,
            "quantity": self.quantity,
            "price" : self.price,
            "total": self.get_total_price(),
            "status": self.status.value,
            "created_data": self.created_data,
            "updated": self.updated,
            "notes": self.notes
        }
    def __str__(self):
        return f"Заказ №{self.order_id} от {self.customer_name} ({self.product} - {self.status.value}) "