#!/usr/bin/env python

class Book():
    def __init__(self, title, year, price):
        self.title = title
        self.year = year
        self.price = price
        self.stock = 100
        self.gain = 0.0
    def sell(self):
        self.stock-=1
        self.gain+= self.price
    def get_title(self):
        return self.title
    def get_year(self):
        return self.year
    def get_price(self):
        return self.price
    def get_stock(self):
        return self.stock
    def get_gain(self):
        return self.gain


B = Book("Hello",1989,20.0)
print(B.title)
B.sell()




