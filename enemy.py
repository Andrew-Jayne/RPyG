from actor import Actor

class Enemy(Actor):
    def __init__(self, name:str, health:int, strength:int, intellect:int, attack_name:str):
        Actor.__init__(self, name=name, health=health, strength=strength, intellect=intellect)
        self.name = name
        self.health = health
        self.strength = strength
        self.intellect = intellect
        self.attack_name = attack_name
        self.attack_power = None

    def set_enemy_attack_power(self):
        if self.strength > self.intellect:
            self.attack_power = self.strength
        else:
            self.attack_power = self.intellect
        return self.attack_power
