# needs a 'pip install scapy'
from scapy.all import ARP, Ether, srp
import socket

def arpscan(add_log,activeScanning):

    # yoinking missy's host ip grabber from scanner.py
    # get local ipv4
    hostname = socket.gethostname()
    address = socket.gethostbyname(hostname)


    target = address + "/" + "24" # change the 24 to the network's CIDR. 

    print("Scanning IP Range: " + target)

    # create ARP broadcast packet
    packet = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=target)
    result = srp(packet, timeout=4, verbose=False)[0]

    for host, received in result:
        try:
            hostname = socket.gethostbyaddr(received.psrc)[0]
        except socket.herror:
            hostname = "Unknown"
        print(f"{received.psrc}  {received.hwsrc}  {hostname}")
    activeScanning[0] = False
