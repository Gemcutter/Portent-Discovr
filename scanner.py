import nmap
import socket
import asyncio
import time

# simple merge sort to re-order the ips for readability
def mergeSortHostByValue(li):
    # if list length is 1 return the list to previous call
    length = len(li)
    if length<2:
        return li
    # split the list in half and send down a layer to sort the smaller lists
    first = mergeSortHostByValue(li[:int(length/2)])
    last = mergeSortHostByValue(li[int(length/2):])
    tmp = []

    for i in range(length):
        # if either array is empty, append the value from the other and skip the remaining code
        if len(first)==0:
            tmp.append(last.pop(0))
            continue
        elif len(last)==0:
            tmp.append(first.pop(0))
            continue
        # split the strings into sub-strings for better sorting
        firstval = first[0][0].split(".")
        lastval = last[0][0].split(".")

        if int(firstval[2])<int(lastval[2]): # sort by third quarter (255.255.!!!.255)
            tmp.append(first.pop(0))
        elif int(firstval[3])<int(lastval[3]): # sort by fourth quarter (255.255.255.!!!)
            tmp.append(first.pop(0))
        else:
            tmp.append(last.pop(0))
    return tmp

def basicScan(add_log):
    # get local ipv4
    hostname = socket.gethostname()
    address = socket.gethostbyname(hostname)

    # break down the ip to get the first 3 quarters only
    address = address.split(".")
    address = ".".join(address[0:3])


    add_log("running - please wait")
    # build scanner
    nm = nmap.PortScanner()
    # init list
    myHostList=[]

    # scan the network for devices
    nm.scan(hosts=address+".1-254", arguments='-sn -n -PS --host-timeout 10ms')
    add_log(address+".1-254 scan complete")
    # get hosts from the scan
    hosts_list = [(x, nm[x]['status']['state']) for x in nm.all_hosts()]
    # sort the ip list
    hosts_list = mergeSortHostByValue(hosts_list) 

    # print the ips and their status
    for host, status in hosts_list:
        add_log(host+': '+status)
        # add ips to secondary scan list
        myHostList.append(host)

    # run a secondary scan to determine operating systems of located devices
    OSguess = nm.scan(hosts=" ".join(myHostList), arguments='-O -p21-25,80,139,443') # -p21-25,80,139,443

    # print the obtained information
    for ip in OSguess["scan"]:
        add_log("ip: "+ip)
        for obj in OSguess["scan"][ip]["osmatch"]:
            add_log("device: "+obj['name']+", accuracy: "+obj['accuracy'])
    # done!
    add_log("Complete")