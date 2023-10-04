class Player:

    def __init__(self, name:str, health:int):
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