from abc import ABC, abstractmethod

class Pizza(ABC):
    @abstractmethod
    def get_price(self):
        pass

class ConcretePizza(Pizza):
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def get_price(self):
        return self.price

class PizzaDecorator(Pizza):
    def __init__(self, pizza):
        self.pizza = pizza
    
    def get_price(self):
        return self.pizza.get_price()

class ConcreteTopping(PizzaDecorator):
    def __init__(self, pizza, name, price):
        super().__init__(pizza)
        self.name = name
        self.price = price

    def get_price(self):
        return super().get_price() + self.price

class PizzaBuilder:
    def __init__(self, name, price, amount):
        self.name = name
        self.amount = amount
        self.pizza = ConcretePizza(name, price)
        self.extension_list = []

    def add_extension(self, name, price):
        self.pizza = ConcreteTopping(self.pizza, name, price)
        self.extension_list.append(name)
		
    def get_price(self):
        return self.pizza.get_price() * self.amount
