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
        "threaded scan": "rangeMin=x.x.x.x rangeMax=x.x.x.x \nintensity=*1-5, up to 7 possible but not recommended*"
    }
    window = tk.Toplevel(root)


    basic_info_label = tk.Label(window, text="basic options info")
    basic_info_label.pack()

    basic_info_textbox = tk.Text(window, height=4)
    basic_info_textbox.pack()
    basic_info_textbox.insert(tk.END, custom_variable_explanations["basic info"])


    passive_label = tk.Label(window, text="passive scan")
    passive_label.pack()

    passive_textbox = tk.Text(window, height=4)
    passive_textbox.pack()
    passive_textbox.insert(tk.END, custom_variable_explanations["passive scan"])



    threaded_label = tk.Label(window, text="threaded scan")
    threaded_label.pack()

    threaded_textbox = tk.Text(window, height=4)
    threaded_textbox.pack()
    threaded_textbox.insert(tk.END, custom_variable_explanations["threaded scan"])