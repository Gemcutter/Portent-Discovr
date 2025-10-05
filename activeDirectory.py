from ldap3 import Server, Connection, ALL
import socket

# Example Inputs
#domainController = 'ADDC01'
#baseDN = 'DC=chris,DC=local'
#username = 'CHRIS\\Administrator'
#password = 'W0nderfu1'

#Needs to return values when called
def queryActiveDirectory(domainController, baseDN, username, password):
    try:
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
                    ip = 'Not found'
            print(f"Name: {name}, DNS: {dns_name}, IP: {ip}, OS: {os}")

    except Exception as e: #If domain is not connected, or incorrect credentials are given
        print(f"Active Directory query failed: {e}")