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


    def _create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
#Меню - Файл->Статистика/выход
        file_menu = tk.Menu(menubar, tearoff= 0)
        menubar.add_cascade(label="Файл", menu=file_menu)
        file_menu.add_command(label ="Статистика", command = " здесь будет команда")
        file_menu.add_command(label="Выход",command="здесь будет команда")
#Меню - Заказы->Новый заказ/обновить список
        order_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Заказы", menu=order_menu)
        order_menu.add_command(label="Новый заказ",command="здесь будет команда")
        order_menu.add_command(label="Обновить список", command="здесь будет команда")
#Меню -      Справка-> о программе
        help_menu = tk.Menu(menubar , tearoff=0)
        menubar.add_cascade(label="Справка", menu=help_menu)
        help_menu.add_command(label="О программе", command="здесь будет команда")

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

        scrollbar = ttk.Scrollbar(middle_frame, orient = tk.VERTICAL , command = "ЗДЕСЬ НАПИСАТЬ КОМАНДУ")
        self.orders_tree.configure(yascrollcommand=scrollbar.set)

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

if __name__ == "__main__":
    root = tk.Tk()
    app = OrderApp(root)
    root.mainloop()
