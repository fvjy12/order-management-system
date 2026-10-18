from order_model import Order, OrderStatus

class OrderManager:
    def __init__(self):
        self.orders = []         
        self.next_order_id = 1   

    def create_order(self, customer_name, product, quantity, price):
        order = Order(self.next_order_id, customer_name, product, quantity, price)
        self.orders.append(order)
        self.next_order_id += 1
        return order

    def get_all_orders(self):
        return self.orders

    def get_order_by_id(self, order_id):
        for order in self.orders:
            if order.order_id == order_id:
                return order
        return None

    def update_order_status(self, order_id, new_status):
        order = self.get_order_by_id(order_id)
        if order:
            order.update_status(new_status)
            return True
        return False

    def delete_order(self, order_id):
        order = self.get_order_by_id(order_id)
        if order:
            self.orders.remove(order)
            return True
        return False

    def add_order_note(self, order_id, note):
        order = self.get_order_by_id(order_id)
        if order:
            order.add_note(note)
            return True
        return False

    def get_orders_by_status(self, status):
        return [order for order in self.orders if order.status == status]

    def get_statistics(self):
        total_orders = len(self.orders)
        
        status_counts = {status.value: 0 for status in OrderStatus}
        for order in self.orders:
            if order.status.value in status_counts:
                status_counts[order.status.value] += 1

        total_revenue = sum(
            order.get_total_price() for order in self.orders 
            if order.status != OrderStatus.CANCELLED
        )

        return {
            "total_orders": total_orders,
            "status_counts": status_counts,
            "total_revenue": total_revenue
        }