# needs a 'pip install scapy'
from scapy.all import ARP, Ether, srp
import socket
import networkDetection
def arpscan(add_log,activeScanning,netMap, user_options=None):

    # yoinking missy's host ip grabber from scanner.py
    # get local ipv4
    hostname = socket.gethostname()
    address = socket.gethostbyname(hostname)


    network = networkDetection.getNetwork() # change the 24 to the network's CIDR. 
    target = network["FullAddress"]


    add_log("Scanning IP Range: " + target)

    # create ARP broadcast packet
    packet = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=target)
    result = srp(packet, timeout=4, verbose=False)[0]

    for host, received in result:
        try:
            hostname = socket.gethostbyaddr(received.psrc)[0]
        except socket.herror:
            hostname = "Unknown"
        add_log(f"{received.psrc}  {received.hwsrc}  {hostname}")
        netMap.addArp(received.psrc,[received.hwsrc,hostname])
    add_log("Scan complete")
    activeScanning[0] = False
