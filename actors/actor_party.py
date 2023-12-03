class Party():
    """
    Stores the progress of the party, and a list/array of member instances 
    """

    def __init__(self, name:str, members:list ) :
        self.progress = 0
        self.name = name
        self.members = members

    def lose_member(self, member_instance):
        pass