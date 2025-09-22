class NetworkMap:
    def __init__(self):
        self.data = {}
        self.identifiedHosts = {}
    def addHost(self, ip, info): 
        if ip in self.data:
            if info != "OS not found" and self.data.get(ip) == "OS not found":
                self.data[ip] = info
                self.identifiedHosts[ip] = info
        else:
            self.data[ip] = info
            if info != "OS not found":
                self.identifiedHosts[ip] = info
            
    def getHost(self, ip):
        return self.data.get(ip)
    def getAllHosts(self):
        return self.data.keys()
    def getRelevantData(self):
        return self.identifiedHosts
    def toString(self):
        stringOut = ""
        for ip in self.data:
            stringOut += f"{ip}, {self.data.get(ip)}\n"
        return stringOut