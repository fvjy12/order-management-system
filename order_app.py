import tkinter as tk 
from tkinter import simpledialog , messagebox , ttk
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
#Меню - Файл->Статистика/выход
        file_menu = tk.Menu(menubar, tearoff= 0)
        menubar.add_cascade(label="Файл", menu=file_menu)
        file_menu.add_command(label ="Статистика", command=self.show_statistics)
        file_menu.add_command(label="Выход",command=self.on_close)
#Меню - Заказы->Новый заказ/обновить список
        order_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Заказы", menu=order_menu)
        order_menu.add_command(label="Новый заказ",command=self.create_new_order)
        order_menu.add_command(label="Обновить список", command=self.refresh_orders_list)
#Меню -      Справка-> о программе
        help_menu = tk.Menu(menubar , tearoff=0)
        menubar.add_cascade(label="Справка", menu=help_menu)
        help_menu.add_command(label="О программе", command=self.show_about)

    def _create_ui(self):
        top_frame = tk.Frame(self.root, padx=10 ,pady=10)
        top_frame.pack(fill=tk.X)

        tk.Label(top_frame, text="Клиент").grid(row=0, column=0,sticky=tk.W, padx=5)
        self.customery_entry = tk.Entry(top_frame, width=15)
        self.customery_entry.grid(row=0, column=1,padx=5)

        tk.Label(top_frame, text="Товар").grid(row=0, column=2, sticky=tk.W,padx=5)
        self.product_entry = tk.Entry(top_frame, width=15)
        self.product_entry.grid(row=0,column=3,padx=5)

        tk.Label(top_frame, text="Кол-во").grid(row=0,column=4, padx=5)
        self.quantity_entry = tk.Entry(top_frame, width=15)
        self.quantity_entry.grid(row=0,column=5,padx=5)

        tk.Label(top_frame, text="Цена").grid(row=0,column=6, padx=5)
        self.price_entry = tk.Entry(top_frame,width=15)
        self.price_entry.grid(row=0, column=7, padx=5)

        self.create_btn = tk.Button(top_frame, text="Создать заказ",command=self.create_new_order, bg="yellow")
        self.create_btn.grid(row=0, column=8, padx=10,pady=5)

        middle_frame = tk.Frame(self.root,padx=10, pady=10)
        middle_frame.pack(fill=tk.BOTH,expand=True)

        tk.Label(middle_frame, text="Список заказов:",font=("Arial", 12,"bold"))    

        columns = ("ID", "Клиент", "Товар", "Кол-во", "Цена", "Итого", "Статус","Дата создание")
        self.orders_tree = ttk.Treeview(middle_frame, columns=columns,show="headings", height=15)           

        self.orders_tree.heading("ID", text = "ID")
        self.orders_tree.heading("Клиент", text = "Клиент")
        self.orders_tree.heading("Товар", text = "Товар")
        self.orders_tree.heading("Кол-во", text = "Кол-во")
        self.orders_tree.heading("Цена", text = "Цена")
        self.orders_tree.heading("Итого", text = "Итого")
        self.orders_tree.heading("Статус", text = "Статус")
        self.orders_tree.heading("Дата создание", text = "Дата создание")  

        self.orders_tree.column("ID", width =50)
        self.orders_tree.column("Клиент", width = 130)
        self.orders_tree.column("Товар", width = 130)
        self.orders_tree.column("Кол-во", width = 70)
        self.orders_tree.column("Цена", width = 80)
        self.orders_tree.column("Итого", width = 80)
        self.orders_tree.column("Статус", width = 150)
        self.orders_tree.column("Дата создание" ,width = 250)

        scrollbar = ttk.Scrollbar(middle_frame, orient = tk.VERTICAL , command = self.orders_tree.yview)
        self.orders_tree.configure(yscrollcommand=scrollbar.set)

        self.orders_tree.pack(side = tk.LEFT, fill = tk.BOTH, expand = True)
        scrollbar.pack(side = tk.RIGHT, fill = tk.Y)


        bottom_frame = tk.Frame(self.root, padx= 10, pady= 10)
        bottom_frame.pack(fill= tk.X)

        self.change_status_btn = tk.Button(
            bottom_frame, 
            text="Изменить статус" ,
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

        self.status_bar = tk.Label(self.root, text="Готово",relief=tk.SUNKEN,anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    # ---------- Методы-обработчики (раздел 5 документации) ----------

    def update_status_bar(self, text):
        self.status_bar.config(text=text)

    def get_selected_order_id(self):
        """Возвращает ID выделенного заказа или None с предупреждением"""
        selection = self.orders_tree.selection()
        if not selection:
            messagebox.showwarning("Внимание", "Сначала выберите заказ в таблице")
            return None
        return int(self.orders_tree.item(selection[0])["values"][0])

    def create_new_order(self):
        """Валидация полей формы + создание заказа (try/except)"""
        customer = self.customery_entry.get().strip()
        product = self.product_entry.get().strip()

        try:
            quantity = int(self.quantity_entry.get())
            price = float(self.price_entry.get().replace(",", "."))
        except ValueError:
            messagebox.showerror("Ошибка", "Поля «Кол-во» и «Цена» должны быть числами")
            return

        if not customer or not product:
            messagebox.showerror("Ошибка", "Заполните поля «Клиент» и «Товар»")
            return
        if quantity <= 0:
            messagebox.showerror("Ошибка", "Количество должно быть больше нуля")
            return
        if price < 0:
            messagebox.showerror("Ошибка", "Цена не может быть отрицательной")
            return

        order = self.order_manager.create_order(customer, product, quantity, price)

        for entry in (self.customery_entry, self.product_entry, self.quantity_entry, self.price_entry):
            entry.delete(0, tk.END)

        self.refresh_orders_list()
        self.update_status_bar(f"Создан заказ №{order.order_id} для {customer}")

    def refresh_orders_list(self):
        """Перерисовка таблицы заказов"""
        for item in self.orders_tree.get_children():
            self.orders_tree.delete(item)

        for order in self.order_manager.get_all_orders():
            values = (
                order.order_id,
                order.customer_name,
                order.product,
                order.quantity,
                f"{order.price:g}",
                f"{order.get_total_price():g}",
                order.status.value,
                order.created_data.strftime("%d.%m.%Y %H:%M")
            )
            self.orders_tree.insert("", tk.END, values=values)

        total = len(self.order_manager.get_all_orders())
        self.update_status_bar(f"Заказов в системе: {total}")

    def change_order_status(self):
        """Диалог выбора нового статуса (модальное окно, раздел 6.4)"""
        order_id = self.get_selected_order_id()
        if order_id is None:
            return
        order = self.order_manager.get_order_by_id(order_id)

        win = tk.Toplevel(self.root)
        win.title(f"Изменение статуса — заказ №{order_id}")
        win.geometry("340x330")
        win.resizable(False, False)
        win.transient(self.root)
        win.grab_set()

        tk.Label(win, text=f"Заказ №{order_id}: {order.customer_name} — {order.product}",
                 wraplength=300, justify=tk.CENTER).pack(pady=(14, 6))
        tk.Label(win, text="Выберите новый статус:", font=("Arial", 10, "bold")).pack(pady=4)

        status_var = tk.StringVar(value=order.status.name)
        for status in OrderStatus:
            tk.Radiobutton(win, text=status.value, value=status.name,
                           variable=status_var).pack(anchor=tk.W, padx=40)

        def apply_status():
            new_status = OrderStatus[status_var.get()]
            self.order_manager.update_order_status(order_id, new_status)
            self.refresh_orders_list()
            self.update_status_bar(f"Статус заказа №{order_id} изменён на «{new_status.value}»")
            win.destroy()

        buttons_frame = tk.Frame(win)
        buttons_frame.pack(pady=14)
        tk.Button(buttons_frame, text="Применить", command=apply_status).pack(side=tk.LEFT, padx=5)
        tk.Button(buttons_frame, text="Отмена", command=win.destroy).pack(side=tk.LEFT, padx=5)

    def add_note_order(self):
        """Диалог ввода заметки к заказу"""
        order_id = self.get_selected_order_id()
        if order_id is None:
            return

        note = simpledialog.askstring("Добавить заметку",
                                      f"Введите заметку к заказу №{order_id}:",
                                      parent=self.root)
        if note and note.strip():
            self.order_manager.add_order_note(order_id, note.strip())
            self.update_status_bar(f"Заметка добавлена к заказу №{order_id}")

    def view_order_details(self):
        """Окно с полной информацией о заказе"""
        order_id = self.get_selected_order_id()
        if order_id is None:
            return
        order = self.order_manager.get_order_by_id(order_id)

        win = tk.Toplevel(self.root)
        win.title(f"Подробности заказа №{order_id}")
        win.geometry("460x360")
        win.transient(self.root)
        win.grab_set()

        details = (
            f"Номер заказа:  {order.order_id}\n"
            f"Клиент:  {order.customer_name}\n"
            f"Товар:  {order.product}\n"
            f"Количество:  {order.quantity}\n"
            f"Цена за единицу:  {order.price:g}\n"
            f"Итого:  {order.get_total_price():g}\n"
            f"Статус:  {order.status.value}\n"
            f"Дата создания:  {order.created_data.strftime('%d.%m.%Y %H:%M')}\n"
            f"Последнее изменение:  {order.updated.strftime('%d.%m.%Y %H:%M')}"
        )
        tk.Label(win, text=details, font=("Arial", 10), justify=tk.LEFT,
                 anchor=tk.W).pack(fill=tk.X, padx=14, pady=(14, 6))

        tk.Label(win, text="Заметки:", font=("Arial", 10, "bold"),
                 justify=tk.LEFT, anchor=tk.W).pack(fill=tk.X, padx=14)

        notes_text = tk.Text(win, height=8, wrap=tk.WORD, state=tk.NORMAL)
        notes_text.pack(fill=tk.BOTH, expand=True, padx=14, pady=6)
        if order.notes:
            notes_text.insert("1.0", order.notes)
        else:
            notes_text.insert("1.0", "Заметок пока нет")
        notes_text.config(state=tk.DISABLED)

        tk.Button(win, text="Закрыть", command=win.destroy).pack(pady=(0, 12))

    def delete_order(self):
        """Удаление заказа с подтверждением (askyesno)"""
        order_id = self.get_selected_order_id()
        if order_id is None:
            return

        if messagebox.askyesno("Удаление заказа",
                               f"Вы уверены, что хотите удалить заказ №{order_id}?"):
            if self.order_manager.delete_order(order_id):
                self.refresh_orders_list()
                self.update_status_bar(f"Заказ №{order_id} удалён")

    def show_statistics(self):
        """Окно со сводной статистикой из OrderManager.get_statistics()"""
        stats = self.order_manager.get_statistics()

        lines = [f"Всего заказов: {stats['total_orders']}", ""]
        for status_value, count in stats["status_counts"].items():
            lines.append(f"  {status_value}: {count}")
        lines.append("")
        lines.append(f"Общая выручка (без отменённых): {stats['total_revenue']:g}")

        messagebox.showinfo("Статистика", "\n".join(lines))

    def show_about(self):
        messagebox.showinfo(
            "О программе",
            "Система учета заказов\n\n"
            "Учебный проект на Python + Tkinter:\n"
            "создание заказов, отслеживание статусов,\n"
            "заметки и статистика."
        )

    def on_close(self):
        """Подтверждение выхода из приложения"""
        if messagebox.askokcancel("Выход", "Закрыть приложение?"):
            self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = OrderApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()
