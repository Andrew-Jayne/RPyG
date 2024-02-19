from message.message import Message

class Combatant():
    def __init__(self, health:int, attack_name:str, attack_power:int, special_attack_name:str) -> None:

        if not isinstance(health, int):
            raise ValueError("The 'health' parameter must be of type int. Received type: {}".format(type(health).__name__))
        if not isinstance(attack_name, str):
            raise ValueError("The 'attack_name' parameter must be of type str. Received type: {}".format(type(attack_name).__name__))
        if not isinstance(attack_power, int):
            raise ValueError("The 'name' parameter must be of type int. Received type: {}".format(type(attack_power).__name__))

        self.health = health
        self.base_health = health

        self.attack_name = attack_name
        self.special_attack_name = special_attack_name
        self.attack_power = attack_power
        
        self.use_special_attack = False
        self.will_react = False
        self.is_dismembered = False

    def damage(self, damage_amount:int) -> None:
        self.health -= damage_amount
        if self.health == 0:
            self.health = 1
            evade_death_message = f"{self.name} has Narrowly Evaded Death!"
            Message.display_message(evade_death_message, 1)
        elif self.health < 0:
            self.health = 0
        health_remaining_message = f"{self.name} has {self.health} Health Remaining"
        Message.display_message(health_remaining_message, 2)
    
    def heal(self, heal_amount:int) -> None:
        self.health += heal_amount
        if self.health > self.base_health:
            self.health = self.base_health
            fully_healed_message = f"{self.name} has Fully Healed!"
            Message.display_message(fully_healed_message, 2)

    def dismember(self) -> None:
        self.is_dismembered = True
        self.attack_power = int(self.attack_power * 0.75)

    def is_fully_healed(self) -> bool:
        return self.health >= self.base_health
    
    def is_alive(self) -> bool:
        if self.health == 0:
            return False
        else:
            return True