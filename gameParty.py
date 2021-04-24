from datetime import datetime
from datetime import timedelta

now = datetime.now()

class gameParty:
    def __init__(self, startTime, duration, maxUsers, owner, id = 0):
        self.startTime = startTime
        self.duration = duration
        self.endTime = startTime + duration
        self.maxUsers = maxUsers
        self.owner = owner
        self.users = []
        self.users.append(owner)
        self.id = id

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
        
        elif joiner in self.users :
            print("This user is already in the party.")
            return -1
        
        else :
            self.users.append(joiner)
            print("Successfully joined the party.")
        

