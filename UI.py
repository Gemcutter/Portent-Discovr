from tkinter import scrolledtext, ttk, messagebox, END, Tk, Menu, WORD, PhotoImage
from customtkinter import CTkInputDialog, CTkToplevel, CTkButton, CTkEntry, CTkLabel, CTkComboBox, set_appearance_mode
from time import localtime
import sys, os

import scanner
import threading
import ArpScanner
import cloudScanner

set_appearance_mode("light")

#name to display and function to use. {name: function}, no scanning functions are available yet so all are set to -1 and nothing accesses the dict
scan_options = {
                "Basic Scan": scanner.basicScan, 
                "Threaded Scan": scanner.threadedScan,
                "Arp Scan": ArpScanner.arpscan, 
                "AWS_scan": cloudScanner.aws_ec2_scan, 
                "Azure_scan": cloudScanner.azure_vm_scan #doesnt work with manually entered credentials?
                }

def resource_path(filename): #to get iconimage working
    if hasattr(sys, "_MEIPASS"):  # Running from PyInstaller bundle
        return os.path.join(sys._MEIPASS, filename)
    return filename  # Running normally


activeScanning = [False]
def execute():
    global activeScanning
    try: #its error time
        if combobox.get():
            selected_scan = combobox.get()
            if selected_scan: #if there is a scan slelcted
                if selected_scan in ["AWS_scan", "Azure_scan"]: #if aws scan chosen
                    if selected_scan == "AWS_scan":
                        results = cloud_login_window("AWS")
                    elif selected_scan == "Azure_scan":
                        results = cloud_login_window("Azure")


                    if results["cancelled"] == 1:
                        add_log("cloud login cancelled by user")
                    else:
                        scan_options[selected_scan](results)

                else:
# --------------------- this method is potentially dodgy and should be revisited. ----------------------
                    if not activeScanning[0]:
                        add_log(f"beginning scan, this might take up to a few minutes")
                        activeScanning[0] = True
                        t = threading.Thread(target=scan_options[selected_scan], args=(add_log,activeScanning,entry.get()))
                        t.start()

    except Exception as e:
        add_log(e)

def on_save():
    if log_box.get("1.0", "end-1c"): #if there is logged content
        name = file_name_query()
        if name:
            add_log(f"Saved to file '{name}' successfully!")

        else:
            add_log("Save cancelled")

def add_log(message):
    log_box.configure(state="normal") #enable temporarily to insert text
    log_box.insert(END, f"{time_now()} - {message}\n") #adds timestamp to line
    log_box.see(END)  # Auto-scroll to bottom
    log_box.configure(state="disabled") #disable again
    root.update_idletasks()

def time_now():
    t = localtime()
    return f"{t.tm_hour}:{t.tm_min}:{t.tm_sec}"

def on_exit():
    root.destroy()

def file_name_query():
    dialog = CTkInputDialog(text="Enter name of file to be saved", title="Save file") #possibly should add a check to see if file exists and warning if overwriting
    return dialog.get_input()

def cloud_login_window(mode): #my own worse CTkInputDialogue with 2 spaces for input
    result = {"access_key": None, 
              "secret_key": None, 
              "location": None,
              "subscription_id": None,
              "cancelled": 0,
              "use_env": 0}

    def ok():
        if mode == "AWS":
            result["access_key"] = access_key_entry.get()
            result["secret_key"] = secret_key_entry.get()
            result["location"] = None#location_menu.get()

        if mode == "Azure":
            result["subscription_id"] = subscription_id_entry.get()
            

        
        window.destroy()

    def cancel():
        result["cancelled"] = 1
        window.destroy()

    def use_env():
        if mode == "Azure":
            result["subscription_id"] = subscription_id_entry.get()
        result["use_env"] = 1
        window.destroy()

    window = CTkToplevel(root)
    window.title(f"{mode} login")
    window.resizable(False,False)
    window.attributes("-topmost", True)

    label = CTkLabel(window, text="Enter cloud credentials. This is not saved")
    if mode == "Azure":
        label = CTkLabel(window, text="Must be logged in with azure cli")
    label.grid(row=0, column=0, columnspan=2, padx=20, pady=20, sticky="ew")
        
    

    if mode == "AWS":
        access_key_entry = CTkEntry(window,placeholder_text="Access Key:")
        secret_key_entry = CTkEntry(window,placeholder_text="Secret Key:")
        access_key_entry.grid(row=1, column=0, columnspan=2, padx=20, pady=(0, 20), sticky="ew")
        secret_key_entry.grid(row=2, column=0, columnspan=2, padx=20, pady=(0, 20), sticky="ew")

        #try to make a scrollable/searchable menu for all aws regions in cloudScanner.locations

    if mode == "Azure":
        subscription_id_entry = CTkEntry(window,placeholder_text="Subscription ID:")
        subscription_id_entry.grid(row=1, column=0, columnspan=2, padx=20, pady=(0, 20), sticky="ew")



    ok = CTkButton(window, text="Ok", command= ok)
    ok.grid(row=7,column=0, padx=(20, 10), pady=(0, 20))

    cancel = CTkButton(window, text="Cancel", command= cancel)
    cancel.grid(row=7,column=1, padx=(10, 20), pady=(0, 20))

    if mode == "AWS":
        env = CTkButton(window, text="Use enviroment variables", command= use_env)
        env.grid(row=8,column=0, padx=(10, 20), pady=(0, 20), columnspan=2) #add colspan

    window.wait_window()
    
    return result

cloudScanner.add_log = add_log # set cloudscanner class output function

# Main window
root = Tk()
root.title("Discovr")
root.geometry("800x500")
root.resizable(False, False)

#change little icon
iconimage = PhotoImage(file=resource_path("compiling\Triskele.png")) #TODO: broken, fix
root.iconphoto(True, iconimage)


# Menu bar
menubar = Menu(root)

filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Save", command=on_save)
filemenu.add_command(label="Exit", command=on_exit)
menubar.add_cascade(label="File", menu=filemenu)

helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="About", command=lambda: messagebox.showinfo(" ", "You wish")) #empty messagebox title due to size restraints
menubar.add_cascade(label="Help", menu=helpmenu)

root.config(menu=menubar)

# Main content frame
content_frame = ttk.Frame(root)
content_frame.pack(fill="both", expand=True, padx=5, pady=5)

# Left panel
left_frame = ttk.Frame(content_frame, width=200)
left_frame.pack(side="left", fill="y")

CTkLabel(left_frame, text="Scan type").pack(anchor="w")

combobox = CTkComboBox(left_frame, values=list(scan_options.keys()), state='readonly', corner_radius=0, border_width=1, border_color="grey")
combobox.set(list(scan_options.keys())[0])
combobox.pack()


# Right panel
right_frame = ttk.Frame(content_frame)
right_frame.pack(side="right", fill="both", expand=True, padx=10)

CTkLabel(right_frame, text="Scan options:").grid(row=0, column=0, sticky="w")
entry = CTkEntry(right_frame, placeholder_text="for selecting arp scan ip target", corner_radius=0, border_width=1, border_color="grey")#ttk.Entry(right_frame)
entry.grid(row=0, column=1, pady=5, sticky="ew")

save_btn = CTkButton(right_frame, text="Save log to file", command= on_save)
save_btn.grid(row=1, column=0, pady=10, sticky="w")

eval_btn = CTkButton(right_frame, text="Scan", command= execute) #no longer insecure :)
eval_btn.grid(row=1, column=1, pady=10, sticky="n")

exit_btn = CTkButton(right_frame, text="Exit", command= on_exit)
exit_btn.grid(row=1, column=2, pady=10, padx=(0,20), sticky="e")

log_box = scrolledtext.ScrolledText( #its the wacky fake terminal log thingymajig
    right_frame,
    wrap=WORD,
    font=("Courier New", 10),
    bg="black",
    fg="lime",
    state="disabled"  # start read-only
)
log_box.grid(row=2, column=0, columnspan=3)



right_frame.columnconfigure(1, weight=1)



if __name__ == "__main__":
    root.mainloop()