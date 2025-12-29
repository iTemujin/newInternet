import client

def readDataBase():

    return None

class Identity():
    def __init__(self):
        self.family = "" # Ipv6
        self.familiar = {} # Kit ismerek
        self.club = {} # Melyik klubban vagyok tag
        self.location = "" # Hova tartozom

        self.role = "", # Milyen szerepem van / volt
        self.uptime = 0 # Mennyi ideje vagyok fent
        self.history = [] # Miket utasitottam már el

class Familiar():
    def __init__(self):
        self.family = "" # Ipv6
        self.attainability = 0 # Elérhetőség 0-100%
        self.club = [] # Melyik klubok tagja
        self.role = "", # Milyen szerepe van / volt
        self.location = "" # Hova tartozik

        self.ping = 0 # Utolsó ping idő atlaga
        self.uptime = 0 # Mennyi ideje van fent
        self.uptime_average = 0 # Átlagos uptime

class Club():
    def __init__(self):
        self.size = 0 # Tagok száma
        self.members = {} # Tagok
        self.location = '' # Hol van a klub

class Member():
    def __init__(self):
        self.family = "" # Ipv6
        self.attainability = 0 # Elérhetőség 0-100%
        self.club = "" # Melyik klubok tagja
        self.role = "" # Milyen szerepe van / volt

        self.ping = 0 # Utolsó ping idő atlaga
        self.uptime = 0 # Mennyi ideje van fent
        self.uptime_average = 0 # Átlagos uptime