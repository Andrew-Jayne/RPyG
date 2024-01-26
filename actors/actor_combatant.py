class Combatant():
    def __init__(self, health:int, attack_name:str, attack_power:int) -> None:
        self.health = health
        self.attack_name = attack_name
        self.attack_power = attack_power
        self.special_attack = None
        self.base_health = health
        self.will_evade = False
        self.will_defend = False
        self.is_poisioned = False
        self.poison_damage = 0
        self.is_dismembered = False

    def damage(self, damage_amount:int) -> None:
        self.health -= damage_amount
        if self.health == 0:
            self.health = 1
            print(f"{self.name} has Narrowly Evaded Death!")
        elif self.health < 0:
            self.health = 0
        print(f"{self.name} has {self.health} Health Remaining", end="\n\n")
    
    def heal(self, heal_amount:int) -> None:
        self.health += heal_amount
        if self.health > self.base_health:
            self.health = self.base_health
            print(f"{self.name} has Fully Healed!")

    def dismember(self) -> None:
        self.is_dismembered = True
        self.attack_power = int(self.attack_power * 0.75)