import sys
import findtag
import client


class Identity():
    def __init__(self, ip):
        self.family = ip # Ipv6
        self.club = None # Melyik klubban vagyok tag (Club vagy None)
        self.location = "" # Hova tartozik

        tags = findtag.find_server()
        if tags is None:
            # Nincs hálózati szerver, létrehozunk egy helyi klubot
            self.club = Club('LocalClub')
            print('No server found — created local club:', self.club.getName())
        else:
            # client.request visszaadja a szerver válaszát (dict) vagy None-t
            data = client.request(tags, 8080, {'request':'can i join'})
            if data is None:
                # Nem kaptunk érvényes választ
                self.club = Club('FallbackClub')
                print('No valid response from server — using fallback club')
            else:
                # Támogatjuk többféle választ: 'request':'yes', 'clubName':..., vagy 'club': 'Name'
                if data.get('request') == 'yes':
                    club_name = data.get('clubName', 'JoinedClub')
                    self.club = Club(club_name)
                    print('Joined club:', self.club.getName())
                elif 'club' in data:
                    self.club = Club(data['club'])
                    print('Club megadva:', self.club.getName())
                else:
                    self.club = Club('UnknownClub')
                    print('Unexpected server response, created:', self.club.getName())

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

