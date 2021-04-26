from datetime import datetime
from datetime import timedelta

class gameParty:
    partyID = 0
    def __init__(self, game, startTime, duration, maxUsers, owner):
        self.startTime = startTime
        self.duration = duration
        self.endTime = startTime + duration
        self.game = game
        self.maxUsers = maxUsers
        self.owner = owner
        self.users = []
        self.users.append(owner)
        self.id = gameParty.partyID
        self.spareUsers = []
        gameParty.partyID = gameParty.partyID + 1
    
    def getStartTime(self):
        return self.startTime

    def partyInfo(self):
        print("Start :", self.startTime)
        print("End Time :", self.endTime)
        print("Maximum Users:", self.maxUsers)
        print("Owner:", self.owner)
        print("Participants:", self.users)

    def partyJoin(self, joiner):
        if len(self.users) == self.maxUsers :
            print("Too many users in this party.")
            return -1
        
        elif joiner in self.users or joiner in self.spareUsers:
            print("This user is already in the party.")
            return -2
        
        else :
            self.users.append(joiner)
            print("Successfully joined the party.")
            return 0
    
    def partyLeave(self, leaver):
        if leaver not in self.users and leaver not in self.spareUsers:
            print("User not in the party.")
            return -1
        
        elif leaver in self.users :
            self.users.remove(leaver)
            print("Successfully left the party.")
            if len(self.spareUsers) > 0 :
                x = self.spareUsers[0]
                self.users.append(x)
                self.spareUsers.remove(x)
            return 0

        elif leaver in self.spareUsers :
            self.spareUsers.remove(leaver)
            return 0



