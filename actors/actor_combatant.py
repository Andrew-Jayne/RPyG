class Combatant():
    def __init__(self, health:int, attack_name:str, attack_power:int) -> None:

        if not isinstance(health, int):
            raise ValueError("The 'health' parameter must be of type int. Received type: {}".format(type(health).__name__))
        if not isinstance(attack_name, str):
            raise ValueError("The 'attack_name' parameter must be of type str. Received type: {}".format(type(attack_name).__name__))
        if not isinstance(attack_power, int):
            raise ValueError("The 'name' parameter must be of type int. Received type: {}".format(type(attack_power).__name__))

        self.health = health
        self.base_health = health

        self.attack_name = attack_name
        self.attack_power = attack_power
        
        self.special_attack = None
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