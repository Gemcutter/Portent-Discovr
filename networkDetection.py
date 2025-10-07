import ipaddress
import socket
from scapy.all import ARP, Ether, srp
import subprocess
import re
import platform

def convertSubnetmaskToCidr(subnet_mask):
    #Converts a subnet mask string (e.g., "255.255.255.0") to its CIDR value (/24).
    octets = subnet_mask.split('.')
    binary_string = ""
    for octet in octets:
        binary_string += bin(int(octet))[2:].zfill(8)
    
    cidr = binary_string.count('1')
    return cidr

def getNetworkRange(cidr):
    network = ipaddress.ip_network(cidr, strict=False)
    return network.network_address, network.broadcast_address

def getNetwork():
    # yoinking missy's host ip detection from scanner.py
    # get local ipv4
    hostname = socket.gethostname()
    address = socket.gethostbyname(hostname)

    # get subnet mask
    # detect OS and run appropriate command - Needs testing on Linux
    if platform.system() == "Windows":
        output = subprocess.check_output("ipconfig", text=True)
        mask_regex = r"Subnet Mask.*?:\s*([\d.]+)"
    else:
        output = subprocess.check_output("ifconfig", text=True)
        mask_regex = r"Mask:([\d.]+)"

    match = re.search(mask_regex, output)
    if match:
        subnetMask = match.group(1)
    else:
        subnetMask = "255.255.255.0" # default to basic subnet mask if not found

    cidr = str(convertSubnetmaskToCidr(subnetMask))
    FullAddress = address +'/'+ cidr
    #print(FullAddress)

    # display network range
    start, end = getNetworkRange(FullAddress)
    #print(f"Network: {FullAddress}")
    #print(f"Subnet mask: {subnetMask}")
    #print(f"Start IP: {start}")
    #print(f"End IP:   {end}")

    return {
        "FullAddress": FullAddress,
        "subnetMask": subnetMask,
        "start": str(start),
        "end": str(end)
    }