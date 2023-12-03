from actors.actor import Actor

class Enemy(Actor):
    def __init__(self, 
                 name:str, 
                 health:int, 
                 strength:int, 
                 intellect:int, 
                 agility:int, 
                 luck:int, 
                 attack_name:str):

        ## Init Inherited Classes     
        Actor.__init__(self, 
                       name=name, 
                       health=health, 
                       strength=strength, 
                       intellect=intellect,
                       agility=agility,
                       luck=luck)

        self.name = name
        self.health = health
        self.strength = strength
        self.intellect = intellect
        self.agility = agility
        self.luck = luck
        self.attack_name = attack_name
        self.attack_power = __class__._set_enemy_attack_power(self)

    def _set_enemy_attack_power(self):
        if self.strength > self.intellect:
            self.attack_power = self.strength
        else:
            self.attack_power = self.intellect
        return self.attack_power
