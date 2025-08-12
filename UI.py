import tkinter as tk


def createWindow():
    root = tk.Tk()

    c = tk.Canvas(root,width=700, height=700)
    c.pack()

    root.mainloop()