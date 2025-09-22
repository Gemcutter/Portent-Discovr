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

def basicScan(add_log, activeScanning, netMap, user_options=None):
    '''
    This function has been made redundant as everything it does is done better by threadedScan()
    '''

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
    OSguess = nm.scan(hosts=myHostList[0], arguments='-O --host-timeout 5000ms') # -A -p- --osscan-guess --version-all -T4 -oN
    
    # print the obtained information
    for ip in OSguess["scan"]:
        add_log("ip: "+ip)
        for obj in OSguess["scan"][ip]["osmatch"]:
            add_log("device: "+obj['name']+", accuracy: "+obj['accuracy'])
    # done!
    add_log("Complete")
    activeScanning[0] = False

# threadedScan will do a primary scan and then complete a secondary scan for each host found,
# threading the secondary scans to run concurrently

def threadedScan(add_log, activeScanning, netMap, user_options=None):
    '''
    args needed for this function are: range and intensity
    '''

    start = time.time()
    add_log("running - please wait")
    
    scanRanges, minSearch, maxSearch = getScanRanges()
    add_log(f"Scan range is from {minSearch} to {maxSearch}")
    nm = nmap.PortScanner()
    myHostList=[]
    # scan each range in scanRanges
    for scanRange in scanRanges:
        add_log("Now scanning range "+scanRange)
        nm.scan(hosts=scanRange, arguments='-sn -n -PS --host-timeout 1000ms')
        add_log(scanRange+" primary scan complete")
        hosts_list = [(x, nm[x]['status']['state']) for x in nm.all_hosts()]
        hosts_list = mergeSortHostByValue(hosts_list) 

        threadList = []
        # print the ips and their status
        for host, status in hosts_list:
            add_log(host+': '+status)
            if status == "up":
                myHostList.append(host)
                t = SecondaryScan(host, nm)
                t.start()
                threadList.append(t)
            
        for t in threadList:
            t.join()
            add_log(" ".join(t.result))
            netMap.addHost(t.result[0],t.result[1])
        add_log("Scan Complete")
    activeScanning[0] = False
    print(f"Execution time: {time.time() - start:.6f} seconds")




# This class is responsible for performing a secondary scan on a single host
class SecondaryScan(threading.Thread):
    def __init__(self, address, nm):
        super().__init__()
        self.result = [address] 
        self.address = address
        self.nm = nm

    def run(self):
        OSguess = self.nm.scan(hosts=self.address, arguments='-O --host-timeout 5000ms -Pn')
        res = ""
        for ip in OSguess["scan"]:
            if 'osmatch' in OSguess["scan"][ip] and len(OSguess["scan"][ip]['osmatch'])>0:
                for obj in OSguess["scan"][ip]['osmatch']:
                    res+="\n - device: "+obj['name']+", accuracy: "+obj['accuracy']+'%'
            else:
                res+="OS not found"
        if len(OSguess["scan"]) < 1:
            res+="OS not found"

        self.result.append(res)

def basicPassiveScan(add_log, activeScanning, netMap, user_options=None):
    '''
    Sniffs at all possible host ips waiting for responses.
    Probably slow as all hell and may require a lot of processing for larger networks.

    args needed for this function: optional range & optional timeout
    '''
    start = time.time()
    
    scanRanges, minSearch, maxSearch = getScanRanges()
    add_log(f"Scan range is from {minSearch} to {maxSearch}")
    nm = nmap.PortScanner()
    threadList = []
    for scanRange in scanRanges:
        add_log("Now scanning range "+scanRange)
        t = PassiveScan(scanRange, nm)
        t.start()
        threadList.append(t)
    
    for t in threadList:
        t.join()
        add_log(t.range+" primary scan complete")
        for ip in t.result:
            if len(t.result[ip]) < 1:
                continue
            if t.result[ip][0]["device"] != "OS not found":
                add_log(f"{ip} is probably {t.result[ip][0]['device']}")
            else:
                add_log(f"{ip} OS is unknown")
            netMap.addHost(ip, t.result[ip])

    activeScanning[0] = False
    print(netMap.toString())
    print(f"Execution time: {time.time() - start:.6f} seconds")






class PassiveScan(threading.Thread):
    def __init__(self, range, nm, timeout=60):
        super().__init__()
        self.result = {}
        self.range = range
        self.nm = nm
        self.timeout = timeout

    def run(self):
        try:
            OSguess = self.nm.scan(hosts=self.range, arguments=f'--packet-trace -O --host-timeout {self.timeout}s')
            for ip in OSguess["scan"]:
                self.result[ip]=[]
                if 'osmatch' in OSguess["scan"][ip] and len(OSguess["scan"][ip]['osmatch'])>0:
                    for obj in OSguess["scan"][ip]['osmatch']:
                        self.result[ip].append({"device": obj['name'], "accuracy": f"{obj['accuracy']}%"})
                else:
                    self.result[ip].append({"device":"OS not found"})
        except Exception as e:
            print(e)
        

        





# This function generates a list of scan ranges based on the provided minimum and maximum IP addresses.
def getRanges(myMin, myMax):
    scanRanges = []
    myMin = myMin.split(".")
    myMax = myMax.split(".")
    for i in range(4):
        myMin[i] = int(myMin[i])
        myMax[i] = int(myMax[i])

    if myMin[2] != myMax[2]:
        for i in range(myMax[2]-myMin[2]+1):
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

# This function returns the default network interface used to connect to a target IP address.
def getDefaultInterface(target: tuple[str, int] | None = None) -> IPv4Interface:
    if target is None:
        target = ("8.8.8.8", 80)
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(target)
            ipAddress = s.getsockname()[0]
    except Exception as e:
        print(f"Failed to auto-detect IP address: {e}")
        ipAddress = "127.0.0.1" 
    try:
        for dev in netifaces.interfaces():
            for items in netifaces.ifaddresses(dev).values():
                for item in items:
                    if item["addr"] == ipAddress:
                        return IPv4Interface(f"{ipAddress}/{item['mask']}")
    except Exception as e:
        print(f"Failed to auto-detect network interface: {e}")
    return IPv4Interface("127.0.0.1/24") 

def getScanRanges():
    hostname = socket.gethostname()
    address = socket.gethostbyname(hostname)
    
    x = getDefaultInterface()
    netmask = x.with_netmask.split('/')[1]
    netmaskBinary = decimalToBinary(netmask.split("."))
    ipBinary = decimalToBinary(address.split("."))
    
    ipBaseBinary = ""
    for i in range(len(netmaskBinary)):
        if int(netmaskBinary[i]) == 1:
            ipBaseBinary+=ipBinary[i]
        else:
            ipBaseBinary+="X"
    
    minSearch = binaryToDecimal(ipBaseBinary.replace("X","0"))
    maxSearch = binaryToDecimal(ipBaseBinary.replace("X","1"))
    
    address = address.split(".")
    address = ".".join(address[0:3])
    
    return [getRanges(minSearch, maxSearch), minSearch, maxSearch]

