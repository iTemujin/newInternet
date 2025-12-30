import sys
import findtag
import client


class Identity():
    def __init__(self, ip):
        self.family = ip # Ipv6
        self.club = {} # Melyik klubban vagyok tag
        self.location = "" # Hova tartozik

        tags = findtag.find_server()
        if tags is None:
            self.club = 'Obj1'
            print('Make club:', self.club)
        else:
            data = client.request(tags, 8080)
            self.club[data['club']] = Club()
            print('Club megadva:', self.club)

    def set_family(self, new_family):
        self.family = new_family
    
    def get_family(self):
        return self.family

class Familiar():
    def __init__(self):
        self.family = "" # Ipv6
        self.club = [] # Melyik klubok tagja
        self.location = "" # Hova tartozik


class Club():
    def __init__(self):
        self.size = 0 # Tagok száma
        self.members = {} # Tagok
        self.location = '' # Hol van a klub

class Member():
    def __init__(self):
        self.family = "" # Ipv6
        self.club = [] # Melyik klubok tagja
        self.location = "" # Hova tartozik

