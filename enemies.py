class Attributes:
    def __init__(self, strength:int, intellect:int):
        self.strength = strength
        self.intellect = intellect
        self.magicka = intellect * 10
        self.stamina = strength * 10

class Enemy(Attributes):

    def __init__(self, name:str, health:int, strength:int, intellect:int, attack:str):
        Attributes.__init__(self, strength=strength, intellect=intellect)
        self.name = name
        self.health = health
        self.attack = attack

    def damage(self, damage_amount:int):
        self.health -= damage_amount
        if self.health == 0:
            self.health = 1
            print(f"The {self.name} Narrowly Evades Death!")
        elif self.health < 0:
            self.health = 0
    
    def heal(self, heal_amount:int):
        self.health += heal_amount
        if self.health > 20:
            self.health = 20
            print(f"The {self.name} is Fully Healed!")