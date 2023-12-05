class Combatant():
    def __init__(self, health:int, ):
        self.health = health
        self.base_health = health
        self.will_evade = False
        self.will_defend = False
        self.aoe_attack = False

    def damage(self, damage_amount:int):
        self.health -= damage_amount
        if self.health == 0:
            self.health = 1
            print(f"{self.name} has Narrowly Evaded Death!")
        elif self.health < 0:
            self.health = 0
        print(f"{self.name} has {self.health} Health Remaining", end="\n\n")
    
    def heal(self, heal_amount:int):
        self.health += heal_amount
        if self.health > self.base_health:
            self.health = self.base_health
            print(f"{self.name} has Fully Healed!")