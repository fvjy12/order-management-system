import tkinter as tk 
from tkinter import simpledialog, messagebox, ttk
from order_model import OrderStatus
from order_manager import OrderManager

class OrderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Система учета заказов")
        self.root.geometry("1000x700")
        
        self.order_manager = OrderManager()

        self._create_menu()
        self._create_ui()
        self.refresh_orders_list()

    def _create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Файл", menu=file_menu)
        file_menu.add_command(label="Статистика", command=self.show_statistics)
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.on_close)

        order_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Заказы", menu=order_menu)
        order_menu.add_command(label="Новый заказ", command=self.create_new_order)
        order_menu.add_command(label="Обновить список", command=self.refresh_orders_list)

        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Справка", menu=help_menu)
        help_menu.add_command(label="О программе", command=self._show_about)

    def _create_ui(self):
        top_frame = tk.Frame(self.root, padx=10, pady=10)
        top_frame.pack(fill=tk.X)

        tk.Label(top_frame, text="Клиент").grid(row=0, column=0, sticky=tk.W, padx=5)
        self.customery_entry = tk.Entry(top_frame, width=15)
        self.customery_entry.grid(row=0, column=1, padx=5)

        tk.Label(top_frame, text="Товар").grid(row=0, column=2, sticky=tk.W, padx=5)
        self.product_entry = tk.Entry(top_frame, width=15)
        self.product_entry.grid(row=0, column=3, padx=5)

        tk.Label(top_frame, text="Кол-во").grid(row=0, column=4, padx=5)
        self.quantity_entry = tk.Entry(top_frame, width=15)
        self.quantity_entry.grid(row=0, column=5, padx=5)

        tk.Label(top_frame, text="Цена").grid(row=0, column=6, padx=5)
        self.price_entry = tk.Entry(top_frame, width=15)
        self.price_entry.grid(row=0, column=7, padx=5)

        self.create_btn = tk.Button(top_frame, text="Создать заказ", command=self.create_new_order, bg="yellow")
        self.create_btn.grid(row=0, column=8, padx=10, pady=5)

        middle_frame = tk.Frame(self.root, padx=10, pady=10)
        middle_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(middle_frame, text="Список заказов:", font=("Arial", 12, "bold")).pack(anchor=tk.W, pady=5)

        columns = ("ID", "Клиент", "Товар", "Кол-во", "Цена", "Итого", "Статус", "Дата создание")
        self.orders_tree = ttk.Treeview(middle_frame, columns=columns, show="headings", height=15)

        self.orders_tree.heading("ID", text="ID")
        self.orders_tree.heading("Клиент", text="Клиент")
        self.orders_tree.heading("Товар", text="Товар")
        self.orders_tree.heading("Кол-во", text="Кол-во")
        self.orders_tree.heading("Цена", text="Цена")
        self.orders_tree.heading("Итого", text="Итого")
        self.orders_tree.heading("Статус", text="Статус")
        self.orders_tree.heading("Дата создание", text="Дата создание")

        self.orders_tree.column("ID", width=50, anchor="center")
        self.orders_tree.column("Клиент", width=130, anchor="w")
        self.orders_tree.column("Товар", width=130, anchor="w")
        self.orders_tree.column("Кол-во", width=70, anchor="center")
        self.orders_tree.column("Цена", width=80, anchor="e")
        self.orders_tree.column("Итого", width=80, anchor="e")
        self.orders_tree.column("Статус", width=150, anchor="center")
        self.orders_tree.column("Дата создание", width=250, anchor="center")

        scrollbar = ttk.Scrollbar(middle_frame, orient=tk.VERTICAL, command=self.orders_tree.yview)
        self.orders_tree.configure(yscrollcommand=scrollbar.set)

        self.orders_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        bottom_frame = tk.Frame(self.root, padx=10, pady=10)
        bottom_frame.pack(fill=tk.X)

        self.change_status_btn = tk.Button(
            bottom_frame, 
            text="Изменить статус",
            command=self.change_order_status
        )
        self.change_status_btn.pack(side=tk.LEFT, padx=5)

        self.add_note_btn = tk.Button(
            bottom_frame,
            text="Добавить заметку",
            command=self.add_note_order
        )
        self.add_note_btn.pack(side=tk.LEFT, padx=5)

        self.view_details_btn = tk.Button(
            bottom_frame,
            text="Подробности",
            command=self.view_order_details
        )
        self.view_details_btn.pack(side=tk.LEFT, padx=5)

        self.delete_btn = tk.Button(
            bottom_frame,
            text="Удалить заказ",
            command=self.delete_order
        )
        self.delete_btn.pack(side=tk.LEFT, padx=5)

        self.status_bar = tk.Label(self.root, text="Готово", relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def create_new_order(self):
        customer = self.customery_entry.get().strip()
        product = self.product_entry.get().strip()
        qty_str = self.quantity_entry.get().strip()
        price_str = self.price_entry.get().strip()

        if not customer or not product or not qty_str or not price_str:
            messagebox.showerror("Ошибка", "Заполните все поля!")
            return

        try:
            quantity = int(qty_str)
            price = float(price_str)
        except ValueError:
            messagebox.showerror("Ошибка", "Количество и цена должны быть числами!")
            return

        self.order_manager.create_order(customer, product, quantity, price)
        
        self.customery_entry.delete(0, tk.END)
        self.product_entry.delete(0, tk.END)
        self.quantity_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)
        
        self.refresh_orders_list()
        self.status_bar.config(text="Заказ успешно создан")

    def refresh_orders_list(self):
        for item in self.orders_tree.get_children():
            self.orders_tree.delete(item)

        for order in self.order_manager.get_all_orders():
            self.orders_tree.insert(
                "", tk.END,
                values=(
                    order.order_id,
                    order.customer_name,
                    order.product,
                    order.quantity,
                    f"{order.price:.2f}",
                    f"{order.get_total_price():.2f}",
                    order.status.value,
                    order.created_data.strftime('%Y-%m-%d %H:%M')
                )
            )

    def get_selected_order_id(self):
        selected = self.orders_tree.selection()
        if not selected:
            messagebox.showwarning("Внимание", "Выберите заказ из таблицы!")
            return None
        return self.orders_tree.item(selected[0])["values"][0]

    def change_order_status(self):
        order_id = self.get_selected_order_id()
        if order_id is None:
            return
        order = self.order_manager.get_order_by_id(order_id)
        if order:
            statuses = list(OrderStatus)
            current_idx = statuses.index(order.status)
            next_status = statuses[(current_idx + 1) % len(statuses)]
            self.order_manager.update_order_status(order_id, next_status)
            self.refresh_orders_list()
            self.status_bar.config(text=f"Статус заказа №{order_id} изменен")

    def add_note_order(self):
        order_id = self.get_selected_order_id()
        if order_id is None:
            return
        note = simpledialog.askstring("Заметка", "Введите текст заметки:")
        if note:
            self.order_manager.add_order_note(order_id, note)
            self.refresh_orders_list()
            self.status_bar.config(text=f"Добавлена заметка к заказу №{order_id}")

    def delete_order(self):
        order_id = self.get_selected_order_id()
        if order_id is None:
            return
        if messagebox.askyesno("Подтверждение", f"Удалить заказ №{order_id}?"):
            if self.order_manager.delete_order(order_id):
                self.refresh_orders_list()
                self.status_bar.config(text=f"Заказ №{order_id} удален")

    def view_order_details(self):
        order_id = self.get_selected_order_id()
        if order_id is None:
            return
        order = self.order_manager.get_order_by_id(order_id)
        if order:
            details = (
                f"ID: {order.order_id}\n"
                f"Клиент: {order.customer_name}\n"
                f"Товар: {order.product}\n"
                f"Количество: {order.quantity}\n"
                f"Цена: {order.price}\n"
                f"Итого: {order.get_total_price()}\n"
                f"Статус: {order.status.value}\n"
                f"Создан: {order.created_data.strftime('%Y-%m-%d %H:%M')}\n\n"
                f"Заметки:\n{order.notes if order.notes else 'Нет заметок'}"
            )
            messagebox.showinfo("Детали заказа", details)

    def show_statistics(self):
        stats = self.order_manager.get_statistics()
        info = f"Всего заказов: {stats['total_orders']}\nВыручка: {stats['total_revenue']:.2f} руб."
        messagebox.showinfo("Статистика", info)

    def _show_about(self):
        messagebox.showinfo("О программе", "Система учета заказов v1.0")

    def on_close(self):
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = OrderApp(root)
    root.mainloop()