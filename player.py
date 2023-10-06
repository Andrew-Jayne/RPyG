class Inventory:
    def __init__(self, gold:int, potions:int):
        self.gold = gold
        self.potions = potions


class Attributes:
    def __init__(self, strength:int, intellect:int):
        self.strength = strength
        self.intellect = intellect
        self.magicka = intellect * 10
        self.stamina = strength * 10


class Combat:
    def __init__(self, strength:int, intellect:int):
        self.strength = strength
        self.intellect = intellect


class Player(Inventory, Attributes, Combat):

    def __init__(self, name:str, health:int, strength:int, intellect:int, gold:int, potions:int):
        Inventory.__init__(self, gold=gold, potions=potions)
        Attributes.__init__(self, strength=strength, intellect=intellect)
        Combat.__init__(self, strength=strength, intellect=intellect)
        self.name = name
        self.health = health

    def damage(self, damage_amount:int):
        self.health -= damage_amount
        if self.health == 0:
            self.health = 1
            print("You Narrowly Escape Death!")
        elif self.health < 0:
            self.health = 0
    
    def heal(self, heal_amount:int):
        self.health += heal_amount
        if self.health > 20:
            self.health = 20
            print("You Are Fully Healed!")


