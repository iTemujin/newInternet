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
            data = client.request(tags, 8080, {'request': 'can I join'})
            if data is not None:
                if data['request'] == 'yes':
                    print('Join', data['clubName'])
            self.club[data['club']] = Club()
            print('Club megadva:', self.club.name())

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
    def __init__(self, name):
        self.name = name
        self.size = 0 # Tagok száma
        self.members = {} # Tagok
        self.location = '' # Hol van a klub
    
    def getName(self):
        return self.name

class Member():
    def __init__(self):
        self.family = "" # Ipv6
        self.club = [] # Melyik klubok tagja
        self.location = "" # Hova tartozik

