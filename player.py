class Player:

    def __init__(self, name:str, health:int):
        self.name = name
        self.health = health

    def damage(self, damage_amount:int):
        self.health -= damage_amount
    
    def heal(self, heal_amount:int):
        self.health += heal_amount