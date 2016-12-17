from Tkinter import *

master = Tk()

var = IntVar()

c = Checkbutton(master, text="Expand", variable=var,  command=lambda: status(var))
c.pack()

def status(var):
    print(var.get())
mainloop()