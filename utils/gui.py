from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from PIL import ImageTk, Image
from datetime import datetime
from utils.decorator import PizzaBuilder
import platform, os

class App(Tk):
    
    def __init__(self, db, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        
        self._frame = None
        self.db = db
        self.switch_frame(StartPage)
        self.title("Pizza Management System")
        if platform.system() == "Windows":
            self.iconbitmap("images/pizza.ico")
        self.shared_data = {"selected_pizza" : IntVar(), "pizza_obj" : list(),"username": "", "password": ""}

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()


class StartPage(Frame):
    def __init__(self, controller):
        Frame.__init__(self, controller)
        self.controller = controller

        self.username = StringVar()
        self.password = StringVar()

        Label(self, text="Welcome to Pizza Management System", font = ('',20),pady = 50).pack()
        Label(self, text="Enter your Login credentials", font = ('',14),pady = 30).pack()

        self.frame = Frame(self)
        self.frame.pack()

        Label(self.frame, text="Username: ", font = ('',10)).grid(row = 0, column = 0)
        Entry(self.frame, textvariable = self.username).grid(row = 0, column = 1)
        Label(self.frame, text="Password: ", font = ('',10)).grid(row = 1, column = 0)
        Entry(self.frame, textvariable = self.password, show = "*").grid(row = 1, column = 1)
        Label(self, text=" ").pack()
        Button(self, text = "Log in", height="2", width="25", command = self.login).pack()
        Label(self, text=" ").pack()
        Button(self, text = "Not Registered? Sign Up!", height="2", width="25", command = lambda: controller.switch_frame(RegistrationPage)).pack()
        Label(self, text=" ").pack() 
        Button(self, text = "Log in as Administrator", height="2", width="25", command = self.admin_login).pack()
        Label(self, text=" ").pack()
        Label(self, text="Admin username and password is 'admin'").pack()

    def login(self):
        self.controller.db.c.execute("SELECT * FROM users WHERE username=? and password=?", (self.username.get(), self.password.get()))
        res = self.controller.db.c.fetchone()
        if res:
            self.controller.shared_data["username"] = self.username.get()
            self.controller.shared_data["password"] = self.password.get()
            self.controller.switch_frame(PizzaMenu)
            if res[2] == 1:
                messagebox.showinfo("Success!", "New Pizzas are added. Check out Pizza menu.")
                self.controller.db.update_notify(self.username.get(), 0)
        else:
            messagebox.showerror("Error!", "Username or password is not correct!")

    def admin_login(self):
        if self.username.get() == "admin" and self.password.get() == "admin":
            self.controller.switch_frame(AdminPage)
        else:
            messagebox.showerror("Error!", "Administrator username or password is not correct!")

class RegistrationPage(StartPage):
    def __init__(self, controller):
        Frame.__init__(self, controller)
        self.controller = controller
        
        self.username = StringVar()
        self.password = StringVar()
        self.re_password = StringVar()

        Label(self, text="Welcome to Pizza Management System", font = ('',20),pady = 50).pack()
        Label(self, text="Enter your Login credentials", font = ('',14),pady = 30).pack()

        self.frame = Frame(self)
        self.frame.pack()

        Label(self.frame, text="Username: ").grid(row = 0, column = 0)
        Entry(self.frame, textvariable = self.username).grid(row = 0, column = 1)
        Label(self.frame, text="Password: ").grid(row = 1, column = 0)
        Entry(self.frame, textvariable = self.password, show = "*").grid(row = 1, column = 1)
        Label(self.frame, text="Re-enter password: ").grid(row = 2, column = 0)
        Entry(self.frame, textvariable = self.re_password, show = "*").grid(row = 2, column = 1)
        Label(self, text="").pack()
        Button(self, text = "Submit", height="2", width="25", command = self.register).pack()
        Label(self, text="").pack()
        Button(self, text = "Back to Login", height="2", width="25", command = lambda: controller.switch_frame(StartPage)).pack()

    def register(self):
        if "" == self.username.get() or "" == self.password.get():
            messagebox.showerror("Error!", "Username or Password cannot be empty!")
            return
        if " " in self.username.get() or " " in self.password.get():
            messagebox.showerror("Error!", "Username or Password cannot include space!")
            return
        if self.password.get() != self.re_password.get():
            messagebox.showerror("Error!", "Passwords do not match!")
            return

        self.controller.db.c.execute("SELECT * FROM users WHERE username = ?", (self.username.get(),))
        if self.controller.db.c.fetchall():
            messagebox.showerror("Error!", "Username is already taken. Try another one.")
        else:
            messagebox.showinfo("Success!", "Account succesfully created!")
            self.controller.db.insert_user(self.username.get(), self.password.get())

class AdminPage(Frame):
    def __init__(self, controller):
        Frame.__init__(self, controller)
        self.controller = controller

        Label(self, text="Administrator Page", font = ('',15), pady = 30).pack()

        self.tree = ttk.Treeview(self)
        self.tree['columns'] = ("User", "Order Price")
        self.tree['height'] = 20
        self.tree.pack()
        self.tree.column("#0", width=150, minwidth=150, stretch = NO)
        self.tree.column("User", width=150, minwidth=150, stretch = NO)
        self.tree.column("Order Price", width=150, minwidth=150, stretch = NO)

        self.tree.heading("#0", text="Order Date")
        self.tree.heading("User", text="User", anchor = W)
        self.tree.heading("Order Price", text="Order Price", anchor = W)

        Label(self, text="").pack()
        Button(self, text = "Add Pizza", height="2", width="25", command = lambda: controller.switch_frame(AddPizza)).pack()
        Label(self, text="").pack()

        Button(self, text = "Go Back", height="2", width="25", command = lambda: controller.switch_frame(StartPage)).pack()
        Label(self, text="").pack()

        self.load_orders()

    def load_orders(self):
        orders = self.controller.db.get_all_orders()
        for i in range(len(orders)):
            self.tree.insert("", "end", text = orders[i][3], values = (orders[i][1], str(orders[i][2]) + "$"))


class AddPizza(Frame):
    def __init__(self, controller):
        Frame.__init__(self, controller)
        self.controller = controller

        self.name_of_pizza = StringVar()
        self.base_price = IntVar()
        self.toppings = StringVar()
        self.topping_prices = StringVar()
        self.image = StringVar()

        Label(self, text="Add Pizza", font = ('',15), pady = 30).pack()
        self.frame = Frame(self)
        self.frame.pack()

        Label(self.frame, text="Name of pizza: ").grid(row = 0, column = 0)
        Entry(self.frame, textvariable = self.name_of_pizza, width = 50).grid(row = 0, column = 1)
        Label(self.frame, text="Base price of pizza: ").grid(row = 1, column = 0)
        Entry(self.frame, textvariable = self.base_price, width = 50).grid(row = 1, column = 1)
        Label(self.frame, text="Toppings seperated by comma: ").grid(row = 2, column = 0)
        Entry(self.frame, textvariable = self.toppings, width = 50).grid(row = 2, column = 1)
        Label(self.frame, text="Corresponding topping prices seperated by comma: ").grid(row = 3, column = 0)
        Entry(self.frame, textvariable = self.topping_prices, width = 50).grid(row = 3, column = 1)
        Label(self.frame, text="Name of image in 'images' folder (.png, .jpg or .jpeg): ").grid(row = 4, column = 0)
        Entry(self.frame, textvariable = self.image, width = 50).grid(row = 4, column = 1)
        Label(self, text=" ").pack()
        Button(self, text = "Submit", height="2", width="25", command = self.add_pizza).pack()
        Label(self, text=" ").pack()
        Button(self, text = "Go back", height="2", width="25", command = lambda: controller.switch_frame(AdminPage)).pack()

    def add_pizza(self):
        self.controller.shared_data["notify"] = True

        if self.name_of_pizza.get() == "" or self.base_price.get() == 0 or self.toppings.get() == "" or \
            self.topping_prices.get() == "" or self.image.get() == "":
            messagebox.showerror("Error!", "Fields cannot be empty!")
        elif os.path.exists("images/" + self.image.get()) == False or \
            self.image.get().lower().endswith(('.png', '.jpg', '.jpeg')) == False:
            messagebox.showerror("Error!", "Image does not exist or does not match requirements!")
        else:
            self.controller.db.insert_pizza(self.name_of_pizza.get(), self.base_price.get(), self.image.get())
            self.pizza_id = self.controller.db.c.lastrowid
        
            topping_list = self.toppings.get()
            topping_list = [ t.strip() for t in topping_list.split(",")]

            price_list = self.topping_prices.get()
            price_list = [ float(p.strip()) for p in price_list.split(",")]

            for i in range(len(topping_list)):
                topping_list[i] = topping_list[i].capitalize()

            for top, price in zip(topping_list, price_list):
                self.controller.db.c.execute("SELECT * FROM toppings WHERE name=? and price=?", (top, price))
                if not self.controller.db.c.fetchall():
                    self.controller.db.insert_topping(top, price)
                    self.topping_id = self.controller.db.c.lastrowid
                    self.controller.db.insert_default_topping(self.pizza_id, self.topping_id)
            

            for user in self.controller.db.get_all_users():
                self.controller.db.update_notify(user[0], 1)
            
            messagebox.showinfo("Success!", "New Pizza succesfully added!")


class PizzaMenu(Frame):
    def __init__(self, controller):
        Frame.__init__(self, controller)
        self.controller = controller
        

        Label(self, text="Pizza Menu", font = ('',15),pady = 30).pack()
        
        Button(self, text = "Log Out", height="2", width="25", command = self.log_out).pack(side=BOTTOM)
        Label(self, text="").pack(side=BOTTOM)
        Button(self, text = "View Order History", height="2", width="25", command = lambda: controller.switch_frame(OrderHistory)).pack(side=BOTTOM)
        Label(self, text="").pack(side=BOTTOM)
        self.controller.db.c.execute("SELECT * FROM pizzas")
        pizzas = self.controller.db.c.fetchall()
        if pizzas != []:
            Button(self, text = "Select", height="2", width="25", command = lambda: controller.switch_frame(PizzaDetails)).pack(side=BOTTOM)
            Label(self, text="").pack(side=BOTTOM)

        self.canvas = Canvas(self)
        self.frame = Frame(self.canvas)
        self.myscrollbar = Scrollbar(self, orient = "vertical", command = self.canvas.yview)
        self.canvas.configure(yscrollcommand = self.myscrollbar.set)

        self.myscrollbar.pack(side="right",fill="y")
        self.canvas.pack()
        self.canvas.create_window((0,0), window = self.frame, anchor='nw')
        self.frame.bind("<Configure>",self.myfunction)
        

        
        if pizzas != []:
            self.controller.shared_data["selected_pizza"].set(pizzas[0][0])
        
        for i in range(len(pizzas)):
            self.show_image("images/" + pizzas[i][3], i)
            Radiobutton(self.frame,font = ('',10), text=pizzas[i][1] + ", " + str(pizzas[i][2]) + "$", \
                variable = self.controller.shared_data["selected_pizza"], value = pizzas[i][0]).grid(row = i, column = 1, sticky=W)
        
    
    def log_out(self):
        self.controller.shared_data = {"selected_pizza" : IntVar(), "pizza_obj" : list(),"username": "", "password": ""}
        self.controller.switch_frame(StartPage)

    def myfunction(self, event):
        self.canvas.configure(scrollregion = self.canvas.bbox("all"), width=450, height=600)

    def show_image(self, name, i):
        self.photo = Image.open(name)
        self.photo = self.photo.resize((175, 175), Image.ANTIALIAS)
        self.image = ImageTk.PhotoImage(self.photo)
        self.l = Label(self.frame, image = self.image)
        self.l.img = self.image
        self.l.grid(row = i, column = 0)
        

class OrderHistory(Frame):
    def __init__(self, controller):
        Frame.__init__(self, controller)
        self.controller = controller

        Label(self, text="Order History", font = ('',15),pady = 30).pack()

        self.tree = ttk.Treeview(self)
        self.tree['columns'] = ("Order Date", "Pizza Name", "Toppings", "Quantity", "Pizza Price", "Order Price")
        self.tree['height'] = 20
        self.tree.pack()
        self.tree.column("#0", width=55, minwidth=55, stretch = NO)
        self.tree.column("Order Date", width=115, minwidth=115, stretch = NO)
        self.tree.column("Pizza Name", width=110, minwidth=110, stretch = NO)
        self.tree.column("Toppings", width=300, minwidth=300, stretch = NO)
        self.tree.column("Quantity", width=60, minwidth=60, stretch = NO)
        self.tree.column("Pizza Price", width=70, minwidth=70, stretch = NO)
        self.tree.column("Order Price", width=70, minwidth=70, stretch = NO)

        self.tree.heading("#0", text="Order ID", anchor = W)
        self.tree.heading("Order Date", text="Order Date", anchor = W)
        self.tree.heading("Pizza Name", text="Pizza Name", anchor = W)
        self.tree.heading("Toppings", text="Toppings", anchor = W)
        self.tree.heading("Quantity", text="Quantity", anchor = W)
        self.tree.heading("Pizza Price", text="Pizza Price", anchor = W)
        self.tree.heading("Order Price", text="Order Price", anchor = W)

        Label(self, text="").pack()
        Button(self, text = "Go Back", height="2", width="25", command = lambda: controller.switch_frame(PizzaMenu)).pack()

        self.load_history()

    def load_history(self):
        self.controller.db.c.execute("SELECT * FROM orders WHERE username=?", (self.controller.shared_data["username"],))
        orders = self.controller.db.c.fetchall()

        for order in orders:
            self.controller.db.c.execute("SELECT * FROM order_details WHERE order_id=?", (order[0],))
            order_detail = self.controller.db.c.fetchall()

            tops = ""
            price = 0
            for i in range(len(order_detail)):
                temp = order_detail[i][1]
                tops += ", " + self.get_topping(order_detail[i][3])[0]
                price += self.get_topping(order_detail[i][3])[1]
                if i + 1 == len(order_detail) or (i + 1 < len(order_detail) and order_detail[i+1][1] != temp):
                    tops = tops[2:]
                    price += self.get_pizza(order_detail[i][1])[1]
                    self.tree.insert("", "end", text = order[0], values = (order[3], self.get_pizza(order_detail[i][1])[0], tops,\
                                    order_detail[i][2], str(price) + "$", str(order[2]) + "$"))
                    tops = ""
                    price = 0
                    if i + 1 != len(order_detail):
                        temp = order_detail[i+1][1]

    def get_pizza(self, pizza_id):
        self.controller.db.c.execute("SELECT * FROM pizzas WHERE pizza_id=?", (pizza_id,))
        res = self.controller.db.c.fetchone()
        return res[1], res[2]

    def get_topping(self, topping_id):
        self.controller.db.c.execute("SELECT * FROM toppings WHERE topping_id=?", (topping_id,))
        res = self.controller.db.c.fetchone()
        if res == None:
            return "", 0
        return res[1], res[2]


class PizzaDetails(Frame): 
    def __init__(self, controller):
        Frame.__init__(self, controller)
        self.controller = controller

        Label(self, text="Toppings", font = ('',15),pady = 30).pack()
		
        self.controller.db.c.execute("SELECT * FROM pizzas WHERE pizza_id=?", (self.controller.shared_data["selected_pizza"].get(),))
        self.selected_pizza = self.controller.db.c.fetchone()

        self.controller.db.c.execute("SELECT * FROM pizza_toppings WHERE pizza_id=?", (self.controller.shared_data["selected_pizza"].get(),))
        self.default_tops = self.controller.db.c.fetchall()
        
        self.vars = []

        for item in range(len(self.default_tops)):
            var = IntVar()
            self.controller.db.c.execute("SELECT * FROM toppings WHERE topping_id=?", (self.default_tops[item][1] ,))
            res = self.controller.db.c.fetchone()
            Checkbutton(self, text = res[1] + "  +" + str(res[2]) + " $", variable = var).pack()
            self.vars.append(var)
        
        self.amount = IntVar(value = 1)
        Label(self, text="").pack()
        self.temp_frame = Frame(self)
        self.temp_frame.pack()
        Label(self.temp_frame, text="Quantity of Pizza: ", font = ('',10)).grid(row = 0, column = 0)
        e = Entry(self.temp_frame, textvariable = self.amount, width="10")
        e.delete(0, END)
        e.insert(0, 1)
        e.grid(row = 0, column = 1)
        

        Label(self, text="").pack()
        Button(self, text = "Apply", height="2", width="25", command = self.state).pack()
        Label(self, text=" ").pack()


        self.price_label = Label(self, text = "")
        self.price_label.pack()

        # if user directly adds to the basket
        self.pizza = PizzaBuilder(self.controller.shared_data["selected_pizza"].get(), self.selected_pizza[2], self.amount.get())

        Label(self, text="").pack()
        Button(self, text = "Add to Basket", height="2", width="25", command = self.add_to_basket).pack()
        
        Label(self, text="").pack()
        self.basket_label = Label(self, text = "", font = ('',10))
        self.basket_label.pack()

        Label(self, text="").pack()
        Button(self, text = "Select another pizza", height="2", width="25", command = lambda: controller.switch_frame(PizzaMenu)).pack()

        Label(self, text="").pack()
        Button(self, text = "Submit", height="2", width="25", command = self.order).pack()

        Label(self, text="").pack()
        self.total_price_label = Label(self, text = "",font = ('',15))
        self.total_price_label.pack()



    def price(self):
        self.price_label['text'] = "Total pizza price : " + str(self.pizza.get_price()) + "$"

    def state(self):
        states = list(map((lambda var: var.get()), self.vars))

        self.pizza = PizzaBuilder(self.controller.shared_data["selected_pizza"].get(), self.selected_pizza[2], self.amount.get())
        for topping, add in zip(self.default_tops, states):
            self.controller.db.c.execute("SELECT * FROM toppings WHERE topping_id=?", (topping[1],))
            top = self.controller.db.c.fetchone()
            if add == 1:
                self.pizza.add_extension(top[0], top[2])
        
        self.price()

    def add_to_basket(self):
        self.controller.shared_data["pizza_obj"].append(self.pizza)
        self.basket_label["text"] = ", ".join([ self.get_pizza_name(pizza.name) + f" x{pizza.amount}" for pizza in self.controller.shared_data["pizza_obj"]])

    def get_pizza_name(self, pizza_id):
        self.controller.db.c.execute("SELECT * FROM pizzas WHERE pizza_id=?", (pizza_id,))
        return self.controller.db.c.fetchone()[1]

    def order(self):
        self.controller.db.insert_order(self.controller.shared_data["username"],\
             sum([pizza.get_price() for pizza in self.controller.shared_data["pizza_obj"]]), datetime.now().replace(microsecond=0))
        self.order_id = self.controller.db.c.lastrowid

        for pizza in self.controller.shared_data["pizza_obj"]:
            if pizza.extension_list != []:
                for topping in pizza.extension_list:               
                    self.controller.db.insert_order_detail(self.order_id, pizza.name, pizza.amount, topping)
            else:
                self.controller.db.insert_order_detail(self.order_id, pizza.name, pizza.amount, 0)

        messagebox.showinfo("Success!", "Your order is succesful")
        
        self.total_price()
        self.controller.shared_data["pizza_obj"] = list()

    def total_price(self):
        self.controller.db.c.execute("SELECT * FROM orders WHERE order_id=?", (self.order_id,))
        order = self.controller.db.c.fetchone()
        self.total_price_label["text"] = "Order Price : " + str(order[2]) + "$"
