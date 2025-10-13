import tkinter as tk
from networkDetection import getNetwork

def options_help(root):
    custom_variable_explanations = {
        "Basic Info": 
        '''Options are (as you may assume) optional. Reasonable defaults will be used if no options are provided. The default network scan range will cover the whole subnet that this device is connected to, but any custom IP range will work, including the normal internet. E.g. from 1.1.1.1 to 1.1.1.254. Note that if using a custom range both a min and a max must be specified, if only one is provided it will be ignored.
Any options to be changed should be done in the following form:
OPTION=VALUE OPTION2=VALUE ...
Each option=value must be seperated by a space. Options ARE case sensitive.
The order of options does not matter''',
        "Passive Scan": "rangeMin=x.x.x.x rangeMax=x.x.x.x \ntimeout=*scan time in seconds*",
        "Active Scan": "rangeMin=x.x.x.x rangeMax=x.x.x.x \nintensity=*0-5*",
        "More about options":"Options rangeMin and rangeMax take an ip formatted as x.x.x.x where each x is an integer between 0 and 255.\n\nOption timeout is a host-timeout option measured in seconds. It will take longer than the entered time as there is other processing after all the packets are received.\n\nOption intensity is a number from 1-5 with 1 being slow and light on the network, to 5 being faster but potentially hard on the network."
    }
    window = tk.Toplevel(root)


    basic_info_label = tk.Label(window, text="Basic Options Info", font=("Arial", 9))
    basic_info_label.pack()

    basic_info_textbox = tk.Text(window, height=9, font=("Arial", 9))
    basic_info_textbox.pack()
    basic_info_textbox.insert(tk.END, custom_variable_explanations["Basic Info"])
    basic_info_textbox.configure(state="disabled",wrap="word")


    passive_label = tk.Label(window, text="Passive Scan", font=("Arial", 9))
    passive_label.pack()

    passive_textbox = tk.Text(window, height=2, font=("Arial", 9))
    passive_textbox.pack()
    passive_textbox.insert(tk.END, custom_variable_explanations["Passive Scan"])
    passive_textbox.configure(state="disabled",wrap="word")



    threaded_label = tk.Label(window, text="Active Scan", font=("Arial", 9))
    threaded_label.pack()

    threaded_textbox = tk.Text(window, height=2, font=("Arial", 9))
    threaded_textbox.pack()
    threaded_textbox.insert(tk.END, custom_variable_explanations["Active Scan"])
    threaded_textbox.configure(state="disabled",wrap="word")

    options_label = tk.Label(window, text="More about options", font=("Arial", 9))
    options_label.pack()

    options_textbox = tk.Text(window, height=8, font=("Arial", 9))
    options_textbox.pack()
    options_textbox.insert(tk.END, custom_variable_explanations["More about options"])
    options_textbox.configure(state="disabled",wrap="word")


def save_help(root):
    text = '''saving will create up to 3 files named NAME.csv, NAME_full_AWS_results.json and NAME_full_logs.txt where NAME is the given name

NAME.csv will only be created if a network scan has been ran. Cloud scans will not add to NAME.csv
NAME_full_AWS_results.json will be a json file containing the full results returned from Amazon
NAME_full_logs.txt will be a text file containing an exact copy of what is visible in the UI log box
'''
    window = tk.Toplevel(root)

    label = tk.Label(window, text="Save/Export details")
    label.pack()

    textbox = tk.Text(window, height=8,wrap="word")
    textbox.pack()
    textbox.insert(tk.END, text)
    textbox.configure(state="disabled")

def info_help(root):
    network = getNetwork()
    window = tk.Toplevel(root)

    text = f'''This computer's IP: {network["FullAddress"]}
Subnet Mask: {network["subnetMask"]}
Network Address: {network["start"]}
Broadcast Address: {network["end"]}
'''

    label = tk.Label(window, text="About your network")
    label.pack()

    textbox = tk.Text(window, height=5,wrap="word", font=("Arial", 9))
    textbox.pack()
    textbox.insert(tk.END, text)
    textbox.configure(state="disabled")

def more_about_scans_window(root):
    cloud_text = '''The AWS scan will print a summary of all ec2 reservations and instances with a more detailed json available to save

The Azure scan only gives a very light summary of VMs and does not support in app authentication, requirering an account logged in to the azure cli to work. THIS SCAN IS EFFECTIVELY NON FUNCTIONAL
'''
    ad_text = '''The active directory query will retrieve details of devices within its domain. This requires both the presence of a domain controller and a set of valid credentials
'''

    window = tk.Toplevel(root)

    cloud_label = tk.Label(window, text="Cloud Scans (AWS and Azure)")
    cloud_label.pack()

    cloud_textbox = tk.Text(window, height=7,wrap="word", font=("Arial", 9))
    cloud_textbox.pack()
    cloud_textbox.insert(tk.END, cloud_text)
    cloud_textbox.configure(state="disabled")


    ad_label = tk.Label(window, text="Active Directory Query")
    ad_label.pack()

    ad_textbox = tk.Text(window, height=3,wrap="word", font=("Arial", 9))
    ad_textbox.pack()
    ad_textbox.insert(tk.END, ad_text)
    ad_textbox.configure(state="disabled")
