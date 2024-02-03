class Actor:
    def __init__(self, 
                 name:str, 
                 strength:int, 
                 intellect:int, 
                 agility:int,
                 luck:int):
        
        if not isinstance(name, str):
            raise ValueError("The 'name' parameter must be of type str. Received type: {}".format(type(name).__name__))
        if not isinstance(strength, int):
            raise ValueError("The 'strength' parameter must be of type int. Received type: {}".format(type(strength).__name__))
        if not isinstance(intellect, int):
            raise ValueError("The 'intellect' parameter must be of type int. Received type: {}".format(type(intellect).__name__))
        if not isinstance(agility, int):
            raise ValueError("The 'agility' parameter must be of type int. Received type: {}".format(type(agility).__name__))
        if not isinstance(luck, int):
            raise ValueError("The 'luck' parameter must be of type int. Received type: {}".format(type(luck).__name__))
        
        self.name = name
        self.strength = strength
        self.intellect = intellect
        self.agility = agility
        self.luck = luck