import tkinter as tk
from tkinter import scrolledtext, ttk, messagebox
import customtkinter
from customtkinter import CTkInputDialog, CTkToplevel
import time


customtkinter.set_appearance_mode("light")


def execute():
    if listbox.curselection():
        selected_scan = listbox.get(listbox.curselection()[0])
        if selected_scan: #if there is a scan slelcted

            if selected_scan in ["AWS_scan", "Azure_scan"]: #if cloud scan chosen
                username, password = cloud_provider_login_window()
                if username == -1:
                        add_log("cloud login cancelled by user")
                elif username and password:
                    add_log(f"username: {username} and password: {password}. !!!this will not be present after this has been properly implimented!!!")
                else:
                    add_log("missing username and/or password")

            else:
                add_log(f"{selected_scan} results as follows: \nlorum ipsum \nqwerty \n1234\n")

def on_save():
    if log_box.get("1.0", "end-1c"): #if there is logged content
        name = file_name_query()
        if name:
            add_log(f"Saved to file '{name}' successfully!")

        else:
            add_log("Save cancelled")

def add_log(message):
    log_box.configure(state="normal") #enable temporarily to insert text
    log_box.insert(tk.END, f"{time_now()} - {message}\n") #adds timestamp to line
    log_box.see(tk.END)  # Auto-scroll to bottom
    log_box.configure(state="disabled") #disable again

def time_now():
    t = time.localtime()
    return f"{t.tm_hour}:{t.tm_min}:{t.tm_sec}"

def on_exit():
    root.destroy()

def file_name_query():
    dialog = CTkInputDialog(text="Enter name of file to be saved", title="Save file") #possibly should add a check to see if file exists and warning if overwriting
    return dialog.get_input()

def cloud_provider_login_window(): #my own worse CTkInputDialogue with 2 spaces for input
    result = {"user": None, "pass": None}

    def ok():
        result["user"] = eusr.get()
        result["pass"] = epswd.get()
        window.destroy()

    def cancel():
        result["user"] = -1
        result["pass"] = -1
        window.destroy()

    window = CTkToplevel(root)
    window.title("Cloud login")
    window.resizable(False,False)
    window.attributes("-topmost", True)

    label = customtkinter.CTkLabel(window, text="Enter login details")
    label.grid(row=0, column=0, columnspan=2, padx=20, pady=20, sticky="ew")

    eusr = customtkinter.CTkEntry(window,placeholder_text="Username:")
    eusr.grid(row=1, column=0, columnspan=2, padx=20, pady=(0, 20), sticky="ew")

    epswd = customtkinter.CTkEntry(window,placeholder_text="Password:")
    epswd.grid(row=2, column=0, columnspan=2, padx=20, pady=(0, 20), sticky="ew")

    ok = customtkinter.CTkButton(window, text="Ok", command= ok)
    ok.grid(row=5,column=0, padx=(20, 10), pady=(0, 20))

    cancel = customtkinter.CTkButton(window, text="Cancel", command= cancel)
    cancel.grid(row=5,column=1, padx=(10, 20), pady=(0, 20))

    window.wait_window()
    
    return result["user"], result["pass"]


# Main window
root = tk.Tk()
root.title("Discovr")
root.geometry("800x500")
root.resizable(False, False)

iconimage = tk.PhotoImage(file = "Triskele.png")
root.iconphoto(True, iconimage)

# Menu bar
menubar = tk.Menu(root)

filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label="Save", command=on_save)
filemenu.add_command(label="Exit", command=on_exit)
menubar.add_cascade(label="File", menu=filemenu)

helpmenu = tk.Menu(menubar, tearoff=0)
helpmenu.add_command(label="About", command=lambda: messagebox.showinfo(" ", "You wish")) #empty title due to size restraints
menubar.add_cascade(label="Help", menu=helpmenu)

root.config(menu=menubar)

# Main content frame
content_frame = ttk.Frame(root)
content_frame.pack(fill="both", expand=True, padx=5, pady=5)

# Left panel
left_frame = ttk.Frame(content_frame, width=200)
left_frame.pack(side="left", fill="y")

ttk.Label(left_frame, text="Scan types").pack(anchor="w")
listbox = tk.Listbox(left_frame, height=10)
listbox.pack()#(fill="y", expand=True)

#name to display and function to use. {name: function}, no scanning functions are available yet so all are set to -1 and nothing accesses the dict
scan_options = {
                "Scan_1": -1, 
                "Scan_2": -1, 
                "Scan_3": -1, 
                "Scan_4": -1, 
                "AWS_scan": -1, 
                "Azure_scan": -1
                }

for item in scan_options:
    listbox.insert("end", item)

# Right panel
right_frame = ttk.Frame(content_frame)
right_frame.pack(side="right", fill="both", expand=True, padx=10)

ttk.Label(right_frame, text="Scan options:").grid(row=0, column=0, sticky="w")
entry = customtkinter.CTkEntry(right_frame, placeholder_text="not currently implimented :(", corner_radius=0, border_width=1, border_color="grey")#ttk.Entry(right_frame)
entry.grid(row=0, column=1, pady=5, sticky="ew")

save_btn = ttk.Button(right_frame, text="Save log to file", command= on_save)
save_btn.grid(row=1, column=0, pady=10, sticky="w")

eval_btn = ttk.Button(right_frame, text="Scan", command= execute) #horrifically insecure, but looks cool, will fix later
eval_btn.grid(row=1, column=1, pady=10, sticky="n")

exit_btn = ttk.Button(right_frame, text="Exit", command= on_exit)
exit_btn.grid(row=1, column=2, pady=10, sticky="e")

log_box = scrolledtext.ScrolledText( #its the wacky fake terminal log thingymajig
    right_frame,
    wrap=tk.WORD,
    font=("Courier New", 10),
    bg="black",
    fg="lime",
    state="disabled"  # Start read-only
)
log_box.grid(row=2, column=0, columnspan=3)



right_frame.columnconfigure(1, weight=1)


# root.mainloop()