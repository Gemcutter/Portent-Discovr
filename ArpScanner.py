# needs a 'pip install scapy'
from scapy.all import ARP, Ether, srp

def arpscan(add_log, args):
    # ip address to scan
    target_ip = "10.136.184.213"  

    if args:
        target_ip = args

    # build packet for both ip and MAC address (it can do both which could be an additional bit of info to have to make us look better)
    arp = ARP(pdst=target_ip)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether/arp

    # send out the packet and capture the response
    result = srp(packet, timeout=2, verbose=0)[0]

    devices = []

    # add each response to the list of devices
    for sent, received in result:
        devices.append({'ip': received.psrc, 'mac': received.hwsrc})

    # print out the list of devices found with IP and MAC address
    for device in devices:
        add_log(f"IP: {device['ip']}, MAC: {device['mac']}")

    add_log("scan complete")