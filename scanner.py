import nmap
import socket
import threading
import time
import netifaces
from ipaddress import IPv4Interface

# simple merge sort to re-order the ips for readability
def mergeSortHostByValue(li):
    
    length = len(li)
    if length<2:
        return li
    
    first = mergeSortHostByValue(li[:int(length/2)])
    last = mergeSortHostByValue(li[int(length/2):])
    tmp = []

    for i in range(length):
        
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

    address = address.split(".")
    address = ".".join(address[0:3])

    add_log("running - please wait")
    # build scanner
    nm = nmap.PortScanner()
    # init list
    myHostList=[]

    # scan the network for devices
    nm.scan(hosts=address+".1-254", arguments='-sn -n -PS --host-timeout 1000ms')
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
    OSguess = nm.scan(hosts=myHostList[0], arguments='-A -p- --osscan-guess --version-all -T4') # -A -p- --osscan-guess --version-all -T4 -oN
    add_log(OSguess)
    # print the obtained information
    for ip in OSguess["scan"]:
        add_log("ip: "+ip)
        for obj in OSguess["scan"][ip]["osmatch"]:
            add_log("device: "+obj['name']+", accuracy: "+obj['accuracy'])
    # done!
    add_log("Complete")


def threadedScan(add_log):
    start = time.time()
    
    hostname = socket.gethostname()
    address = socket.gethostbyname(hostname)
    
    x = get_default_interface()
    netmask = x.with_netmask.split('/')[1]
    netmaskBinary = decimalToBinary(netmask.split("."))
    
    wipeKey = 0
    for i in range(len(netmaskBinary)):
        if int(netmaskBinary[i]) == 1:
            wipeKey = i+1
    padding0 = ""
    padding1 = ""
    for i in range(32-wipeKey):
        padding0+="0"
        padding1+="1"
    minSearch = decimalToBinary(address.split("."))[:wipeKey]+padding0
    maxSearch = decimalToBinary(address.split("."))[:wipeKey]+padding1
    minSearch = binaryToDecimal(minSearch)
    maxSearch = binaryToDecimal(maxSearch)


    address = address.split(".")
    address = ".".join(address[0:3])

    scanRanges = getScanRanges(minSearch, maxSearch)

    add_log("running - please wait")
    nm = nmap.PortScanner()
    myHostList=[]
    for scanRange in scanRanges:
        nm.scan(hosts=scanRange, arguments='-sn -n -PS --host-timeout 1000ms')
        add_log(scanRange+" primary scan complete")
        hosts_list = [(x, nm[x]['status']['state']) for x in nm.all_hosts()]
        hosts_list = mergeSortHostByValue(hosts_list) 

        threadList = []

        for host, status in hosts_list:
            add_log(host+': '+status)
            myHostList.append(host)
            t = MyThread(host, nm)
            t.start()
            threadList.append(t)

        for t in threadList:
            t.join()
            add_log(t.result)
    print(f"Execution time: {time.time() - start:.6f} seconds")


    
class MyThread(threading.Thread):
    def __init__(self, address, nm):
        super().__init__()
        self.result = address+" OS not found"
        self.address = address
        self.nm = nm

    def run(self):
        OSguess = self.nm.scan(hosts=self.address, arguments='-O --host-timeout 5000ms')
        res = self.address+" OS not found"
        for ip in OSguess["scan"]:
            res=ip
            if 'osmatch' in OSguess["scan"][ip] and len(OSguess["scan"][ip]['osmatch'])>0:
                for obj in OSguess["scan"][ip]['osmatch']:
                    res+="\n - device: "+obj['name']+", accuracy: "+obj['accuracy']+'%'
            else:
                res+=" OS not found"
            

        self.result = res
    
    
def getScanRanges(myMin, myMax):
    scanRanges = []
    myMin = myMin.split(".")
    myMax = myMax.split(".")
    if myMin[2] != myMax[2]:
        for i in range(myMax[2]-myMin[2]):
            scanRanges.append(f"{myMin[0]}.{myMin[1]}.{myMin[2]+i}.1-254")
    else:
        scanRanges.append(f"{myMin[0]}.{myMin[1]}.{myMin[2]}.{myMin[3]}-{myMax[3]}")
    return scanRanges

def decimalToBinary(n):
    li = ''
    for i in n:
        li+=str(format(int(i), f'0{8}b'))
    return li

def binaryToDecimal(n):
    n = [n[0:8],n[8:16],n[16:24],n[24:32]]
    li = ''
    for i in n:
        sum = 0
        for j in range(8):
            sum += int(i[j])*2**(7-j)
        li+=str(sum)+"."
    return li[:len(li)-1]

def get_default_interface(target: tuple[str, int] | None = None) -> IPv4Interface:
    """Return the network interface used to connect to target."""
    if target is None:
        target = ("8.8.8.8", 80)  # Google DNS server address
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(target)
            ip_address = s.getsockname()[0]
    except Exception as e:
        print(f"Failed to auto-detect IP address: {e}")
        ip_address = "127.0.0.1"  # fallback to localhost
    try:
        for dev in netifaces.interfaces():
            for items in netifaces.ifaddresses(dev).values():
                for item in items:
                    if item["addr"] == ip_address:
                        return IPv4Interface(f"{ip_address}/{item['mask']}")
    except Exception as e:
        print(f"Failed to auto-detect network interface: {e}")
    return IPv4Interface("127.0.0.1/24")  # fallback to localhost
