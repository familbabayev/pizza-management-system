import sqlite3


class DB:
    def __init__(self, db_file):
        self.db_file = db_file
        self.conn = sqlite3.connect(self.db_file)
        self.c = self.conn.cursor()
        self.c.execute("CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY NOT NULL, password TEXT NOT NULL, notify INTEGER)")
        self.c.execute("CREATE TABLE IF NOT EXISTS pizzas (pizza_id INTEGER PRIMARY KEY NOT NULL, name TEXT, base_price REAL, image TEXT)")
        self.c.execute("CREATE TABLE IF NOT EXISTS toppings (topping_id INTEGER PRIMARY KEY NOT NULL, name TEXT, price REAL)")

        self.c.execute("CREATE TABLE IF NOT EXISTS default_pizza (pizza_id INTEGER REFERENCES pizzas(pizza_id), topping_id INTEGER REFERENCES toppings(topping_id))")

        self.c.execute("CREATE TABLE IF NOT EXISTS orders (order_id INTEGER PRIMARY KEY NOT NULL, \
            username INTEGER REFERENCES users(username), total_price REAL, datetime TEXT)")
    
        self.c.execute("CREATE TABLE IF NOT EXISTS order_details (order_id INTEGER REFERENCES orders(order_id), \
            pizza_id INTEGER REFERENCES pizzas(pizza_id), amount INTEGER, \
                topping_id INTEGER REFERENCES toppings(topping_id))")
    
    def insert_user(self, username, password):
        with self.conn:
            self.c.execute("INSERT INTO users VALUES (?, ?, ?)", (username, password, 0))
            
    def search_user(self, username):
        self.c.execute("SELECT * FROM users WHERE username=?", (username,))
        return self.c.fetchall()
            
    def update_password(self, username, new_password):
        with self.conn:
            self.c.execute("UPDATE users SET password=? WHERE username=?", (new_password, username))

    def delete_user(self, username):
        with self.conn:
            self.c.execute("DELETE from users WHERE username=?", (username,))

    def update_notify(self, username, state):
        with self.conn:
            self.c.execute("UPDATE users SET notify=? WHERE username=?", (state, username))
    
    def get_all_users(self):
        with self.conn:
            self.c.execute("SELECT * FROM users")
        return self.c.fetchall()
    
    ########

    def insert_pizza(self, name, base_price, image):
        with self.conn:
            self.c.execute("INSERT INTO pizzas VALUES (NULL, ?, ?, ?)", (name, round(base_price, 2), image))

    def get_all_pizzas(self):
        with self.conn:
            self.c.execute("SELECT * FROM pizzas")
        return self.c.fetchall()

    ########

    def insert_topping(self, name, price):
        with self.conn:
            self.c.execute("INSERT INTO toppings VALUES (NULL, ?, ?)", (name, round(price,2)))

    def get_all_toppings(self):
        with self.conn:
            self.c.execute("SELECT * FROM toppings")
        return self.c.fetchall()   
        
    ########

    def insert_order(self, username, total_price, datetime):
        with self.conn:
            self.c.execute("INSERT INTO orders VALUES (NULL, ?, ?, ?)", (username, total_price, datetime))

    def get_all_orders(self):
        with self.conn:
            self.c.execute("SELECT * FROM orders")
        return self.c.fetchall()

    ########
    def insert_default_topping(self, pizza_id, topping_id):
        with self.conn:
            self.c.execute("INSERT INTO default_pizza VALUES (?, ?)", (pizza_id, topping_id))

    def get_all_default_toppings(self):
        with self.conn:
            self.c.execute("SELECT * FROM default_pizza")
        return self.c.fetchall()

    ########

    def insert_order_detail(self, order_id, pizza_id, amount, topping_id):
        with self.conn:
            self.c.execute("INSERT INTO order_details VALUES (?, ?, ?, ?)", (order_id, pizza_id, amount, topping_id))

    def get_all_records(self):
        with self.conn:
            self.c.execute("SELECT * FROM order_details")
        return self.c.fetchall()