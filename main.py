from utils.decorator import PizzaBuilder
from utils.database import DB
from utils.gui import App
from datetime import datetime


db = DB("pizza.db")

#those are the sample database records already in database.
'''
db.insert_user("test", "123")
db.insert_user("a", "a")

db.insert_pizza("Chicken Ranch", 13, "chicken_ranch.jpg")
pizza_id1 = db.c.lastrowid
db.insert_pizza("Chicken BBQ", 15, "chicken_barbekyu.jpg")
pizza_id2 = db.c.lastrowid
db.insert_pizza("Mexicano", 12, "meksika.jpg")
pizza_id3 = db.c.lastrowid
db.insert_pizza("Pepperoni", 14, "klassik_pepperoni.jpg")
pizza_id4 = db.c.lastrowid
db.insert_pizza("Orleans", 16, "new_orleans_pizza.jpg")
pizza_id5 = db.c.lastrowid

db.insert_topping("Pepperonchini", 1.5)
topping_id_1 = db.c.lastrowid
db.insert_topping("Mozzarella", 2.5)
topping_id_2 = db.c.lastrowid
db.insert_topping("Tomatoes", 1.5)
topping_id_3 = db.c.lastrowid
db.insert_topping("Grilled Chicken", 2)
topping_id_4 = db.c.lastrowid
db.insert_topping("Fresh Mushrooms", 1.5)
topping_id_5 = db.c.lastrowid
db.insert_topping("Jalapeno", 1)
topping_id_6 = db.c.lastrowid
db.insert_topping("Black Olives", 1)
topping_id_7 = db.c.lastrowid
db.insert_topping("Corn", 1.6)
topping_id_8 = db.c.lastrowid
db.insert_topping("Green Peppers", 1)
topping_id_9 = db.c.lastrowid
db.insert_topping("Fresh Mushrooms", 2.5)
topping_id_10 = db.c.lastrowid

db.insert_default_topping(pizza_id1, topping_id_1)
db.insert_default_topping(pizza_id1, topping_id_2)
db.insert_default_topping(pizza_id1, topping_id_3)
db.insert_default_topping(pizza_id1, topping_id_4)

db.insert_default_topping(pizza_id2, topping_id_5)
db.insert_default_topping(pizza_id2, topping_id_1)
db.insert_default_topping(pizza_id2, topping_id_2)
db.insert_default_topping(pizza_id2, topping_id_4)

db.insert_default_topping(pizza_id3, topping_id_5)
db.insert_default_topping(pizza_id3, topping_id_6)
db.insert_default_topping(pizza_id3, topping_id_1)
db.insert_default_topping(pizza_id3, topping_id_2)
db.insert_default_topping(pizza_id3, topping_id_3)
db.insert_default_topping(pizza_id3, topping_id_4)

db.insert_default_topping(pizza_id4, topping_id_1)
db.insert_default_topping(pizza_id4, topping_id_2)
db.insert_default_topping(pizza_id4, topping_id_7)

db.insert_default_topping(pizza_id5, topping_id_10)
db.insert_default_topping(pizza_id5, topping_id_1)
db.insert_default_topping(pizza_id5, topping_id_8)
db.insert_default_topping(pizza_id5, topping_id_2)
db.insert_default_topping(pizza_id5, topping_id_4)
db.insert_default_topping(pizza_id5, topping_id_9)

db.insert_order("test", 34.9, datetime.now().replace(microsecond=0))
db.insert_order("a", 36, datetime.now().replace(microsecond=0))

db.insert_order_detail(1, 1, 1, 1)
db.insert_order_detail(1, 1, 1, 2)
db.insert_order_detail(1, 1, 1, 4)
db.insert_order_detail(1, 3, 1, 6)
db.insert_order_detail(1, 3, 1, 1)
db.insert_order_detail(1, 3, 1, 3)
db.insert_order_detail(2, 1, 1, 0)
db.insert_order_detail(2, 5, 1, 10)
db.insert_order_detail(2, 5, 1, 8)
db.insert_order_detail(2, 5, 1, 4)
db.insert_order_detail(2, 5, 1, 9)
'''

#print("All users: ", db.get_all_users())
#print("All default toppings: ",db.get_all_default_toppings())
#print("All pizzas: ",db.get_all_pizzas())
#print("All toppings: ",db.get_all_toppings())
#print("All orders: ",db.get_all_orders())
#print("All : ",db.get_all_records())


app = App(db)
app.geometry('800x900')
app.mainloop()











