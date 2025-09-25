import socket
import subprocess

def get_domain_controller():
    try:
        # Use nslookup to find the domain controller via _ldap._tcp.dc._msdcs DNS query
        result = subprocess.check_output(['nslookup', '-type=SRV', '_ldap._tcp.dc._msdcs'], universal_newlines=True)
        controllerFound = False
        for line in result.splitlines():
            if 'svr hostname' in line or 'service' in line:
                # Extract the hostname from the line
                parts = line.split()
                for part in parts:
                    if '.' in part:
                        controllerFound = True
                        return part
        if not controllerFound:
            return "No domain controller (possibly not on a domain)"
        # Fallback: Try to get domain controller via environment variable
        domain_controller = socket.gethostbyname_ex(socket.getfqdn())[0]
        return domain_controller
    
    except Exception as errorMessage:
        return f"Error finding domain controller: {errorMessage}"

if __name__ == "__main__": #change to function later
    domainController = get_domain_controller()
    print(f"Active Domain Controller: {domainController}")