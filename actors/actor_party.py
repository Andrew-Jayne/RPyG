class Party():
    """
    Stores the progress of the party, and a list/array of member instances 
    """

    def __init__(self, members:list ) :
        self.progress = 0
        self.members = members

    def lose_member(self, member_instance):
        pass