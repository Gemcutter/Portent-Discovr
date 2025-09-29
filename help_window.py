import tkinter as tk

def options_help(root):
    custom_variable_explanations = {
        "basic info": 
        '''any options to be changed should be done in the following form:
OPTION=VALUE OPTION2=VALUE
each option=value must be seperated by a space. options ARE case sensitive.
the order of each options does not matter
''',
        "passive scan": "rangeMin=x.x.x.x rangeMax=x.x.x.x \ntimeout=*scan time in seconds*",
        "active scan": "rangeMin=x.x.x.x rangeMax=x.x.x.x \nintensity=*1-5, up to 7 possible but not recommended*"
    }
    window = tk.Toplevel(root)


    basic_info_label = tk.Label(window, text="basic options info")
    basic_info_label.pack()

    basic_info_textbox = tk.Text(window, height=4)
    basic_info_textbox.pack()
    basic_info_textbox.insert(tk.END, custom_variable_explanations["basic info"])
    basic_info_textbox.configure(state="disabled")


    passive_label = tk.Label(window, text="passive scan")
    passive_label.pack()

    passive_textbox = tk.Text(window, height=4)
    passive_textbox.pack()
    passive_textbox.insert(tk.END, custom_variable_explanations["passive scan"])
    passive_textbox.configure(state="disabled")



    threaded_label = tk.Label(window, text="threaded scan")
    threaded_label.pack()

    threaded_textbox = tk.Text(window, height=4)
    threaded_textbox.pack()
    threaded_textbox.insert(tk.END, custom_variable_explanations["active scan"])
    threaded_textbox.configure(state="disabled")

def save_help(root):
    text = '''saving will create up to 2 files named NAME.csv and NAME_full_logs.txt where NAME is the given name

NAME.csv will only be created if a network scan has been ran. Cloud scans will not add to NAME.csv
NAME_full_logs.txt will be a text file containing an exact copy of what is visible in the UI log box
'''
    window = tk.Toplevel(root)

    label = tk.Label(window, text="Save/Export details")
    label.pack()

    textbox = tk.Text(window, height=8,wrap="word")
    textbox.pack()
    textbox.insert(tk.END, text)
    textbox.configure(state="disabled")