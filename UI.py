import tkinter as tk

def createWindow():
    root = tk.Tk()
    root.resizable(False, False)
    root.title("Discovr UI")

    #basic ui shape blocked out with frames | total dimentions are 1000x700
    topbar = tk.Frame(root,width=1000, height=50, background="yellow")
    leftmenu = tk.Frame(root,width=200, height=650, background="red")
    mainblock = tk.Frame(root,width=800, height=550, background="blue")
    submenu = tk.Frame(root,width=800, height=100, background="green")

    #place frames in window
    topbar.grid(row= 0, column= 0, columnspan=2)
    leftmenu.grid(row= 1, column= 0, rowspan=2)
    mainblock.grid(row= 2, column= 1)
    submenu.grid(row= 1, column= 1)



    root.mainloop()
