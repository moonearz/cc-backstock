import tkinter as tk

class app(tk.Tk):
    def __init__(self):
        super().__init__()

win = app()
win.geometry("500x500")
win.title("Order Guide")

outer_frame = tk.Frame(win)
outer_frame.pack(fill = "both", expand = 1)

in_canvas = tk.Canvas(outer_frame)

scroller = tk.Scrollbar(outer_frame, orient = "vertical", command = in_canvas.yview)
scroller.pack(side = "right", fill = "y")

in_canvas.configure(yscrollcommand = scroller.set)
in_canvas.bind('<Configure>', lambda e: in_canvas.configure(scrollregion = in_canvas.bbox("all")))

in_frame = tk.Frame(in_canvas, width = 1000, height = 100)
btn1 = tk.Button(in_frame, text = "test", fg = "blue", width = 22, font = ("bold", 10), height = 1)
btn1.place(x = 600, y = 0)

in_canvas.create_window((0, 0), window = in_frame, anchor = "nw")

win.mainloop()
