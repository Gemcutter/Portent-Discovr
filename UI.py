import tkinter as tk
from tkinter import scrolledtext, ttk, messagebox
import time

def on_item_select(event):
    selected = listbox.curselection()
    if selected:
        item = listbox.get(selected[0])
        entry_var.set(item)
        add_log(f"Selected '{item}'")

def on_save():
    name = entry_var.get()
    if name.strip() and (name.strip() not in saved_expressions):
        listbox.insert("end", name)
        saved_expressions.append(name.strip())
        add_log(f"Saved '{name}' successfully!")

    elif name.strip():
        messagebox.showwarning("Warning", "Item already exists")

    else:
        messagebox.showwarning("Warning", "Field cannot be empty.")

def add_log(message):
    # Enable temporarily to insert text
    log_box.configure(state="normal")
    log_box.insert(tk.END, f"{message}\n")
    log_box.see(tk.END)  # Auto-scroll to bottom
    log_box.configure(state="disabled")

def time_now():
    t = time.localtime()
    return f"{t.tm_hour}:{t.tm_min}"

def on_exit():
    root.destroy()

# Main window
root = tk.Tk()
root.title("Discovr")
root.geometry("800x500")
root.resizable(False, False)

iconimage = tk.PhotoImage(file = "Triskele.png")
root.iconphoto(True, iconimage,)


# Menu bar
menubar = tk.Menu(root)
filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label="Save", command=on_save)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=on_exit)
menubar.add_cascade(label="File", menu=filemenu)

helpmenu = tk.Menu(menubar, tearoff=0)
helpmenu.add_command(label="About", command=lambda: messagebox.showinfo("About", "Sample Tkinter App v1.0"))
menubar.add_cascade(label="Help", menu=helpmenu)

root.config(menu=menubar)

# Main content frame
content_frame = ttk.Frame(root)
content_frame.pack(fill="both", expand=True, padx=5, pady=5)

# Left panel
left_frame = ttk.Frame(content_frame, width=200)
left_frame.pack(side="left", fill="y")

ttk.Label(left_frame, text="Expressions").pack(anchor="w")
listbox = tk.Listbox(left_frame, height=10)
listbox.pack(fill="y", expand=True)


saved_expressions = ["'hello world'", "3**2", "saved_expressions", "time_now()"]
for item in saved_expressions:
    listbox.insert("end", item)
listbox.bind("<<ListboxSelect>>", on_item_select)

# Right panel
right_frame = ttk.Frame(content_frame)
right_frame.pack(side="right", fill="both", expand=True, padx=10)

ttk.Label(right_frame, text="Input:").grid(row=0, column=0, sticky="w")
entry_var = tk.StringVar()
entry = ttk.Entry(right_frame, textvariable=entry_var)
entry.grid(row=0, column=1, pady=5, sticky="ew")

save_btn = ttk.Button(right_frame, text="Save as expression", command=on_save)
save_btn.grid(row=1, column=0, pady=10, sticky="w")

eval_btn = ttk.Button(right_frame, text="Eval", command= lambda: add_log(f"{entry_var.get()} evaluated as: {eval(entry_var.get())}")) #horrifically insecure, but looks cool
eval_btn.grid(row=1, column=1, pady=10, sticky="n")

exit_btn = ttk.Button(right_frame, text="Exit", command=on_exit)
exit_btn.grid(row=1, column=2, pady=10, sticky="e")

log_box = scrolledtext.ScrolledText(
    right_frame,
    wrap=tk.WORD,
    font=("Courier New", 10),
    bg="black",
    fg="lime",
    state="disabled"  # Start read-only
)
log_box.grid(row=2,column=0, columnspan=3)

right_frame.columnconfigure(1, weight=1)

# Status bar
status = tk.StringVar(value="Ready")
status_bar = ttk.Label(root, textvariable=status, relief="sunken", anchor="w")
status_bar.pack(side="bottom", fill="x")

root.mainloop()
