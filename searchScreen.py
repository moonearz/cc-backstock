import tkinter as tk
import tkinter.ttk as tkk
from tkinter import messagebox

class searchScreen():
    def __init__(self, master, products):
        self.master = master
        self.itemList = products
        self.backstock = master.backstock
        self.add_screen = tk.Toplevel()
        self.add_screen.title("search dialog")
        self.add_screen.rowconfigure(138)
        self.add_screen.columnconfigure(3)
        self.display = []
        tk.Label(master = self.add_screen, text = "Enter a product name or SKU: ").grid(row = 0, column = 0, columnspan = 2)
        self.input = tk.Entry(master = self.add_screen)
        self.input.grid(row = 0, column = 2)
        self.add_screen.bind('<Return>', self.hitReturn)
    
    def destroy(self):
        self.add_screen.destroy()

    def buildButton(self, rowNumber, text, sku):
        tk.Label(master = self.add_screen, text = text).grid(row = rowNumber, column = 0, sticky = "w")
        tk.Label(master = self.add_screen, text = sku).grid(row = rowNumber, column = 1, sticky = "w")
        tk.Button(master = self.add_screen, text = "Add", command = lambda: self.master.addItem(sku, self), bg = "green").grid(row = rowNumber, column = 2, sticky = "nsew")

    def hitReturn(self, event):
        searchValue = self.input.get()
        if searchValue.isdigit():
            self.destroy()
            self.skuSearch(self.backstock, searchValue)
        else:
            self.SearchAlgo(self.itemList, searchValue)

    def SearchAlgo(self, candidates, entry):
        if entry == "":
            pass
        else:
            copy = candidates.copy()
            for item in candidates:
                if entry.lower() not in candidates[item][0].lower():
                    copy.pop(item)
            if len(copy) == 0:
                self.destroy()
                prompt = messagebox.askquestion("error: no results found", "Try again?", icon = "error")
                if prompt == 'yes':
                    self.__init__(self.master, self.itemList)
            else:
                results_label = tk.Label(master = self.add_screen, text = "Results found:")
                results_label.grid(row = 1, column = 0, sticky = "w")
                sku_label = tk.Label(master = self.add_screen, text = "SKU")
                sku_label.grid(row = 1, column = 1, sticky = "w")
                for index, item in enumerate(copy):
                    self.buildButton(index + 2, copy[item][0], item)
                
    def skuSearch(self, backstock, entry):
        if entry in backstock:
            prompt = messagebox.askquestion("error: already in backstock", "Try again?", icon = "error")
            if prompt == 'yes':
                self.__init__(self.master, self.itemList)
            else:
                pass
        else:
            if entry in self.itemList:
                prompt = messagebox.askyesno("item found", "Add " + self.itemList[entry][0] + " to backstock?")
                if prompt:
                    self.master.addItem(entry, self)
            else:
                prompt = messagebox.askquestion("item not found", "Try again?", icon = "error")
                if prompt == 'yes':
                    self.__init__(self.master, self.itemList)