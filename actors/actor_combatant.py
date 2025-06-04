from utilites.utilities import ensure_type


class Combatant:
    def __init__(
        self, health: int, attack_name: str, attack_power: int, special_attack_name: str
    ) -> None:
        ensure_type(health, int, "health")
        ensure_type(attack_name, str, "attack_name")
        ensure_type(attack_power, int, "attack_power")
        # ensure_type(special_attack_name, str, 'special_attack_name')

        self.health = health
        self.base_health = health

        self.attack_name = attack_name
        self.special_attack_name = special_attack_name
        self.special_attack_energy = 2
        self.attack_power = attack_power

        self.use_special_attack = False
        self.will_react = False
        self.is_dismembered = False

    def damage(self, damage_amount: int) -> None:
        ensure_type(damage_amount, int, "damage_amount")

        from message.message import Message

        self.health -= damage_amount
        if self.health == 0:
            self.health = 1
            evade_death_message = f"{self.name} has Narrowly Evaded Death!"
            Message.display_message(evade_death_message, 1)
        elif self.health < 0:
            self.health = 0
        health_remaining_message = f"{self.name} has {self.health} Health Remaining"
        Message.display_message(health_remaining_message, 2)

    def heal(self, heal_amount: int) -> None:
        ensure_type(heal_amount, int, "heal_amount")

        from message.message import Message

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
