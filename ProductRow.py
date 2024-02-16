import tkinter as tk
import tkinter.ttk as tkk

"""
This class encapsulates a product's row in the window
"""

class ProductRow():
    def __init__(self, SKU, window, products, rowNumber):
        self.master = window
        self.sku = SKU
        self.name = products[SKU][0]
        self.price = products[SKU][1]
        self.quantity = products[SKU][2]
        self.rowNumber = rowNumber
        self.value = "1"

        #Labels
        self.labels = []
        self.ilabel = tk.Label(master = window, text = products[SKU][0])
        self.slabel = tk.Label(master = window, text = f"{SKU}")
        self.qlabel = tk.Label(master = window, text = "1")
        self.plabel = tk.Label(master = window, text = products[SKU][1])
        self.labels.append(self.ilabel)
        self.labels.append(self.slabel)
        self.labels.append(self.plabel)
        self.labels.append(self.qlabel)

        #Buttons
        self.buttons = []
        self.abutton = tk.Button(master = window, text = "+", command = lambda i= rowNumber - 1: self.increase(), bg = "green")
        self.pbutton = tk.Button(master = window, text = u'\u2202', command = lambda i= rowNumber - 1: self.partial(), bg = "yellow")
        self.dbutton = tk.Button(master = window, text = "-", command = lambda i= rowNumber - 1: self.decrease(), bg = "red")
        self.ddbutton = tk.Button(master = window, text = u'\uD83D\uDDD1', command = lambda i=rowNumber - 1: self.delete(), bg = "orange")
        self.buttons.append(self.abutton)
        self.buttons.append(self.pbutton)
        self.buttons.append(self.dbutton)
        self.buttons.append(self.ddbutton)

    def setLabelValue(self, value):
        self.qlabel["text"] = value
        self.value = value
    
    def getValue(self):
        return self.value

    def delete(self):
        for label in self.labels:
            label.destroy()
        for button in self.buttons:
            button.destroy()
        self.master.removeBackstock(self.sku, self.rowNumber)

    def getSKU(self):
        return self.sku
    
    def getName(self):
        return self.name

    def getPrice(self):
        return self.price

    def getQuantity(self):
        return self.quantity
    
    def addLabels(self):
        for index, label in enumerate(self.labels):
            if(index == 3):
                label.grid(row = self.rowNumber, column = 5)
            else:
                label.grid(row = self.rowNumber, column = index)

            
    def addButtons(self):
        for index, button in enumerate(self.buttons):
            if(index < 2):
                button.grid(row = self.rowNumber, column = index + 3, sticky = "nsew")
            else:
                button.grid(row = self.rowNumber, column = index + 4, sticky = "nsew")
    
    def increase(self):
        #check if value is partial to make addition/subtraction compatible
        if '.' in self.qlabel["text"]:
            is_part = True
            self.qlabel["text"] = self.qlabel["text"][:-2]
        else:
            is_part = False
        value = int(self.qlabel["text"])
        self.qlabel["text"] = f"{value + 1}"
        if is_part:
            self.qlabel["text"] = self.qlabel["text"] + ".5"
        self.value = self.qlabel["text"]
        self.master.updateTime()

    def decrease(self):
        #check if value is partial to make addition/subtraction compatible
        if '.' in self.qlabel["text"]:
            is_part = True
            self.qlabel["text"] = self.qlabel["text"][:-2]
        else:
            is_part = False
        value = int(self.qlabel["text"]) - 1
        if(value > 0):
            self.qlabel["text"] = f"{value}"
        #delete if value is zero or below zero
        elif((value == 0  and not is_part) or value < 0):
            self.delete()
            return
        if is_part:
            self.qlabel["text"] = f"{value}" + ".5"
        self.value = self.qlabel["text"]
        self.master.updateTime()

    def partial(self):
        if '.' in self.qlabel["text"]:
            self.qlabel["text"] = self.qlabel["text"][:-2]
            if int(self.qlabel["text"]) == 0:
                self.delete()
        else: 
            self.qlabel["text"] = self.qlabel["text"] + ".5"
        self.value = self.qlabel["text"]
        self.master.updateTime()

