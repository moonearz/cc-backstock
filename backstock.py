import tkinter as tk
import tkinter.ttk as tkk
from tkinter import messagebox
import io
import csv
from ProductRow import ProductRow
from searchScreen import searchScreen
from datetime import datetime
import pdb
from pathlib import Path

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()   
        self.rowNumber = 1
        #dictionary of ProductRow objects, keys are row indices
        self.Rows = {}
        self.backstock = {}

    def setLabels(self):
        self.lbl_item = tk.Label(master = self, text = "Product Name" )
        self.lbl_item.grid(row = 0, column = 0)
        self.lbl_SKU = tk.Label(master = self, text = "SKU")
        self.lbl_SKU.grid(row = 0, column = 1)
        self.lbl_quantity = tk.Label(master = self, text = "Quantity")
        self.lbl_quantity.grid(row = 0, column = 5)
        self.lbl_price = tk.Label(master = self, text = "Price")
        self.lbl_price.grid(row = 0, column = 2)
        #buttons for clearing the backstock and adding new things to the backstock, sorting the backstock
        self.add_button = tk.Button(master = self, text = "Add Backstock", command = self.addBackstock, bg = "light blue")
        self.clear_button = tk.Button(master = self, text = "Clear Backstock", command = self.clearRows, bg = "salmon")
        self.add_button.grid(row = 150, column = 0, columnspan = 4, sticky = "nsew")
        self.clear_button.grid(row = 150, column = 4, columnspan = 4, sticky = "nsew")
        self.sort_by_sku = tk.Button(master = self, text = "Sort by SKU", command = self.sortBySKU, bg = "blue")
        self.sort_by_sku.grid(row = 0, column = 8, sticky = "nsew")
        self.sort_alpha = tk.Button(master = self, text = "Sort Alphabetically", command = self.sortAlpha, bg = "purple")
        self.sort_alpha.grid(row = 0, column = 9, sticky = "nsew")
        #last updated label
        self.sys_update_time = update_time
        self.last_updated_label = tk.Label(master = self, text = "Last updated on: ")
        self.last_updated_label.grid(row = 150, column = 8, sticky = "nse")
        self.time_label = tk.Label(master = self, text = self.sys_update_time)
        self.time_label.grid(row = 150, column = 9, sticky = "wns")
    
    def sortBySKU(self):
        prs = self.Rows.values()
        skus = []
        for p in prs:
            skus.append((p.getSKU(), p.getValue()))
        skus = sorted(skus)
        for i in self.Rows.copy():
                self.Rows[i].delete()
        for key, val in skus:
            self.backstock[key] = products[key]
            trow = self.getRowNumber()
            current = ProductRow(key, self, products, trow)
            self.setRow(trow, current)
            current.addLabels()
            current.setLabelValue(val)
            current.addButtons()
            self.incrementRow()  
            

    def sortAlpha(self):
        prs = self.Rows.values()
        names = []
        for p in prs:
            names.append((p.getName(), p.getValue(), p.getSKU()))
        names = sorted(names)
        for i in self.Rows.copy():
                self.Rows[i].delete()
        for name, val, sku in names:
            self.backstock[sku] = products[sku]
            trow = self.getRowNumber()
            current = ProductRow(sku, self, products, trow)
            self.setRow(trow, current)
            current.addLabels()
            current.setLabelValue(val)
            current.addButtons()
            self.incrementRow() 

    def updateTime(self):
        time = datetime.now().strftime('%m/%d/%Y at %I:%M %p')
        self.time_label["text"] = time
        self.sys_update_time = time

    def getRowNumber(self):
        return self.rowNumber
    
    def incrementRow(self):
        self.rowNumber += 1
    
    def setRow(self, index, product):
        self.Rows[index] = product
    
    def addBackstock(self):
        searchScreen(self, products)

    def removeBackstock(self, SKU, rowNumber):
        self.backstock.pop(SKU)
        self.Rows.pop(rowNumber)
        self.rowNumber -= 1
        self.updateTime()

    def addItem(self, SKU, searchScreen):
        if SKU not in self.backstock:
            searchScreen.destroy()
            addition = ProductRow(SKU, self, products, self.rowNumber)
            self.Rows[self.rowNumber] = addition
            addition.addLabels()
            addition.addButtons()
            self.backstock[SKU] = products[SKU]
            self.rowNumber += 1
            self.updateTime()
        else:
            searchScreen.destroy()
            error = messagebox.askquestion("error: already in backstock", "Try again?", icon = "error")
            if error == 'yes':
                self.addBackstock()

    def clearRows(self):
        sure = messagebox.askyesno("check", "Are you sure?", icon = "warning")
        if sure:
            for i in self.Rows.copy():
                self.Rows[i].delete()
            self.Rows = {}
            self.rowNumber = 1
            self.updateTime()
        
#create main window
window = MainWindow()
window.title("Backstock Tracker")

#this is a dictionary that maps skus to a list of product name, price, quantity
products = {}
p = Path(__file__).with_name('cookie_candy_products.txt')
database = open(p, "r")
with database as csvfile:
    linereader = csv.DictReader(csvfile, delimiter = ',')
    for row in linereader:
        products[row['SKU']] = [row['Product Name'], row['Price'], row['Quantity/case']]

#read current backstock file and make dictionary of current backstock
cb = Path(__file__).with_name('current_backstock.txt')
startup_backstock = open(cb, "r")
with startup_backstock as csvfile:
    r = csv.DictReader(csvfile, delimiter = ',')
    for row in r:
        if '/' in row['SKU']:
            update_time = row['SKU']
        else:
            window.backstock[row['SKU']] = [row['Product Name'], row['Price'], row['Quantity/case'], row['Current Quantity']]

#read items in from saved backstock
for index, item in enumerate(window.backstock):
    trow = window.getRowNumber()
    current = ProductRow(item, window, products, trow)
    window.setRow(index + 1, current)
    current.addLabels()
    current.setLabelValue(window.backstock[item][3])
    current.addButtons()
    window.incrementRow()

window.rowconfigure(150, minsize = 100, weight = 1)
window.columnconfigure(9, minsize = 100, weight = 1)
window.setLabels()

window.mainloop()

#write current backstock to current_backstock file
with open(cb, "w+") as f:
    f.write("SKU,Product Name,Price,Quantity/case,Current Quantity" + "\n")
    for index, key in enumerate(window.Rows):
        p = window.Rows[key]
        f.write(p.getSKU() + ',' + p.getName() +',' + p.getPrice() + ',' + p.getQuantity() + ',' + p.getValue())
        if(index <= len(window.Rows) - 1):
            f.write("\n")
    f.write(window.sys_update_time)
f.close()