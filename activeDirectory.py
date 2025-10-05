from ldap3 import Server, Connection, ALL
import socket

# Example Inputs
#domainController = 'ADDC01' or '192.168.20.10' Enter IP address
#baseDN = 'DC=chris,DC=local' chris.local 
#username = 'CHRIS\\Administrator' DOMAIN\\username
#password = 'W0nderfu1' password

#Needs to return values when called
def queryActiveDirectory(add_log, activeScanning, netMap, inputs):
  
    try:
        domainController = inputs["domainController"]
        baseDN = inputs["baseDN"]
        username = inputs["username"]  
        password = inputs["password"]

        add_log(f'{domainController}, {baseDN}, {username}, {password}')
        server = Server(domainController, get_info=ALL)
        conn = Connection(server, user=username, password=password, auto_bind=True)
        conn.search(baseDN, '(objectClass=computer)', attributes=['name', 'dNSHostName', 'operatingSystem'])

        for entry in conn.entries:
            name = entry.name.value
            dns_name = entry.dNSHostName.value if 'dNSHostName' in entry else None
            os = entry.operatingSystem.value if 'operatingSystem' in entry else 'OS not found'
            ip = None
            if dns_name:
                try:
                    ip = socket.gethostbyname(dns_name)
                except Exception:
                    ip = 'IP not found'
            add_log(f"IP: {ip}, Name: {name}, OS: {os}") #adds IP, Hostname and OS
            netMap.addAQQ(ip, name, os) 
    except Exception as e: #If domain is not connected, or incorrect credentials are given
        add_log(f"Active Directory query failed: {e}")

    activeScanning[0] = False
