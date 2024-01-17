class Party:
    def __init__(self, members):
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
        if not isinstance(name, str):
            ValueError("The 'name' parameter must be of type str. Received type: {}".format(type(name).__name__))
        if not isinstance(members, list):
            raise ValueError("The 'members' parameter must be of type list. Received type: {}".format(type(members).__name__))

        Party.__init__(self, members=members)
        self.progress = 0
        self.name = name
        self.members = members


class EnemyParty(Party):
    def __init__(self, name:str, members:list):
        if not isinstance(name, str):
            ValueError("The 'name' parameter must be of type str. Received type: {}".format(type(name).__name__))
        if not isinstance(members, list):
            raise ValueError("The 'members' parameter must be of type list. Received type: {}".format(type(members).__name__))
        
        Party.__init__(self, members=members)
        self.name = name
        self.members = members