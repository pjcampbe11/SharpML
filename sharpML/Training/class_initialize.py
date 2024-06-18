#!/usr/bin/env python

class Book():
    def __init__(self,title, year, price = 20.0, notes = None):
        """
        builder function for the class Book

        Parameters
        -----------
        title (str): title of the book
        ...
        ...
        """
        self.title = title
        self.year = year
        self.price = price
        if notes is not None:
            self.notes = notes
        else:
            self.notes = "No notes for this book"
        self.fruit = {}
    def get_title(self):
        return self.title
    
B = Book("Hello","1989",43.2)
print(B.title)
B2 = Book("Dodo","2003")
print(B2.get_title())

