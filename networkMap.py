class NetworkMap:
    def __init__(self):
        self.data = {
        "nameNMAC":{},
        "devNAcc":{},
        "ADQ":{}
        }
        self.identifiedHosts = {}
        self.continueScanning = True
    def addArp(self, ip, info):
        if ip in self.data["nameNMAC"]:
            if info[1] != "Unknown" and self.data["nameNMAC"].get(ip)[1] == "Unknown":
                self.data["nameNMAC"][ip] = info
        else:
            self.data["nameNMAC"][ip] = info
            if info[1] != "Unknown":
                self.identifiedHosts[ip] = info
    def addHost(self, ip, info): 
        if ip in self.data["devNAcc"]:
            if info[0] != "OS not found" and self.data["devNAcc"].get(ip)[0] == "OS not found":
                self.data["devNAcc"][ip] = info
                self.identifiedHosts[ip] = info
        else:
            self.data["devNAcc"][ip] = info
            if info[0] != "OS not found":
                self.identifiedHosts[ip] = info
    def addADQ(self, ip, name, os):
        self.data["ADQ"][ip] = [name, os]
    def getHost(self, ip):
        return self.data["devNAcc"].get(ip)
    def getAllHosts(self):
        return self.data["devNAcc"].keys()
    def getRelevantData(self):
        return self.identifiedHosts
    def toString(self):
        stringOut=""
        if len(self.data["devNAcc"].keys())>0:
            stringOut += "Active/Passive Scan\nip, device, accuracy"
            for ip in self.data["devNAcc"]:
                    stringOut+=f'\n{ip}, {self.data["devNAcc"].get(ip)[0]}, {self.data["devNAcc"].get(ip)[1]}'
        if len(self.data["nameNMAC"].keys())>0:
            if len(self.data["devNAcc"].keys())>0:
                stringOut += "\n"
            stringOut += "Arpscan\nip, MAC, hostname"
            for ip in self.data["nameNMAC"]:
                stringOut+=f'\n{ip}, {self.data["nameNMAC"].get(ip)[0]}, {self.data["nameNMAC"].get(ip)[1]}'
        if len(self.data["ADQ"].keys())>0:
            if len(self.data["nameNMAC"].keys())>0:
                stringOut += "\n"
            stringOut += "Active Directory Query\nip, name, os"
            for ip in self.data["ADQ"]:
                stringOut+=f'\n{ip}, {self.data["ADQ"].get(ip)[0]}, {self.data["ADQ"].get(ip)[1]}'
        return stringOut