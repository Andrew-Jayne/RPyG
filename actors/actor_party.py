class Party():
    def __init__(self, members:list):

        self.members = members

    def lose_member(self, member):
        self.members.remove(member)
    
    def gain_member(self, member):
        self.members.append(member)

class PlayerParty(Party):
    """
    Stores the progress of the party, and a list/array of member instances 
    """

    def __init__(self, name:str, members:list):

        Party.__init__(self, members=members)
        self.progress = 0
        self.name = name
        self.members = members


class EnemyParty(Party):
    def __init__(self, members:list):

        Party.__init__(self, members=members)
        self.members = members