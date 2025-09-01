import ipaddress
import socket
from scapy.all import ARP, Ether, srp

# manual ip address to scan,currenly not in use
#target_ip = "10.136.249.0/24"  

def subnet_mask_to_cidr(subnet_mask):
    #Converts a subnet mask string (e.g., "255.255.255.0") to its CIDR value.
    octets = subnet_mask.split('.')
    binary_string = ""
    for octet in octets:
        # Convert each octet to its 8-bit binary representation
        binary_string += bin(int(octet))[2:].zfill(8)
    
    # Count the number of '1's to get the CIDR value
    cidr = binary_string.count('1')
    return cidr

def get_network_range(cidr):
    network = ipaddress.ip_network(cidr, strict=False)
    return network.network_address, network.broadcast_address

# yoinking missy's host ip grabber from scanner.py
# get local ipv4
hostname = socket.gethostname()
address = socket.gethostbyname(hostname)

subnetMask = "255.255.128.0"  # Uni subnet mask = "255.255.128.0", need to find a way to get this dynamically. Worst case, can get client to just run ipconfig and enter it in manually
cidr = str(subnet_mask_to_cidr(subnetMask))
FullAddress = address +'/'+ cidr
print(FullAddress)

start, end = get_network_range(FullAddress)
print(f"Network: {FullAddress}")
print(f"Start IP: {start}")
print(f"End IP:   {end}")