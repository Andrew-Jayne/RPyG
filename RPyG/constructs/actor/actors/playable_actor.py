import random

from RPyG.constructs.actor.actor_components import Inventory
from RPyG.constructs.actor.actors.combatant_actor import CombatantActor
from RPyG.utilities import ensure_type


class PlayableActor(CombatantActor):
    react_action: str
    react_messages: dict[str, str]
    inventory: Inventory
    __slots__: tuple[str, ...] = ("react_action", "react_messages", "inventory")

    @classmethod
    def build(
        cls,
        name: str,
        specialization: str,
    ) -> PlayableActor:
        ensure_type(name, str, "name")
        ensure_type(specialization, str, "specialization")
        match specialization:
            case "WARRIOR":
                strength = random.randint(5, 10)
                intellect = random.randint(1, 5)
                agility = random.randint(4, 8)
                luck = random.randint(1, 10)
            case "MAGE":
                strength = random.randint(1, 5)
                intellect = random.randint(5, 10)
                agility = random.randint(4, 8)
                luck = random.randint(1, 10)
            case "ROGUE":
                strength = random.randint(4, 8)
                intellect = random.randint(4, 8)
                agility = random.randint(5, 10)
                luck = random.randint(1, 10)
            case _:
                raise ValueError(f"Error Invalid Specialization {specialization}")
        react_messages = PlayableActor._get_react_action(specialization, name)

        player_health = (strength + intellect) * 10
        return cls(
            name=name,
            specialization=specialization,
            strength=strength,
            intellect=intellect,
            agility=agility,
            luck=luck,
            health=player_health,
            base_health=player_health,
            inventory=Inventory(
                gold=strength * 25,
                potions=int(intellect / 2),
                actor_name=name,
            ),
            react_action=react_messages[0],
            react_messages=react_messages[1],
            attack_name=PlayableActor._get_attack_name(specialization),
            attack_power=PlayableActor._get_attack_power(
                specialization,
                strength,
                intellect,
                agility,
            ),
            special_attack_name=PlayableActor._get_special_attack(specialization),
        )

    def __init__(
        self,
        name: str,
        specialization: str,
        strength: int,
        intellect: int,
        agility: int,
        luck: int,
        inventory: Inventory,
        react_action: str,
        react_messages: dict[str, str],
        health: int,
        base_health: int,
        attack_name: str,
        attack_power: int,
        special_attack_name: str,
        use_special_attack: bool = False,
        will_react: bool = False,
        is_dismembered: bool = False,
        special_attack_energy: int = 0,
    ) -> None:
        ensure_type(name, str, "name")
        ensure_type(specialization, str, "specialization")
        ensure_type(strength, int, "strength")
        ensure_type(intellect, int, "intellect")
        ensure_type(agility, int, "agility")
        ensure_type(luck, int, "luck")
        ensure_type(inventory, Inventory, "inventory")
        ensure_type(react_action, str, "react_action")
        ensure_type(react_messages, dict, "react_messages")
        for key, value in react_messages.items():
            ensure_type(key, str, "key")
            ensure_type(value, str, "value")
        ensure_type(health, int, "health")
        ensure_type(attack_name, str, "attack_name")
        ensure_type(attack_power, int, "attack_power")
        ensure_type(special_attack_name, str, "special_attack_name")

        self.react_action = react_action
        self.react_messages = react_messages
        self.inventory = inventory

        CombatantActor.__init__(
            self,
            name=name,
            strength=strength,
            intellect=intellect,
            agility=agility,
            luck=luck,
            health=health,
            base_health=base_health,
            attack_name=attack_name,
            attack_power=attack_power,
            special_attack_name=special_attack_name,
            specialization=specialization,
        )

    def use_potion(self, ignore_fully_healed: bool = False) -> Inventory.PotionResult:
        from RPyG.core_io import CoreIO, output_models

        core_io = CoreIO.get_core_io()
        if self.inventory.potions != 0 and (
            self.is_fully_healed() is False or ignore_fully_healed is True
        ):
            self.inventory.lose_potion(1)
            heal_magnitude = 100 + random.randint(-20, 20)
            self.heal(heal_magnitude)
            core_io.send_output(
                output_models.UsePotionMessage(
                    actor_name=self.name,
                    potions_used=1,
                    heal_amount=heal_magnitude,
                    potions_remaining=self.inventory.potions,
                    fully_healed=self.is_fully_healed(),
                    ignore_fully_healed=ignore_fully_healed,
                )
            )

            return Inventory.PotionResult(
                success=True,
                no_potions=False,
                fully_healed=self.is_fully_healed(),
            )
        if (
            self.inventory.potions != 0
            and self.is_fully_healed() is True
            and ignore_fully_healed is False
        ):
            core_io.send_output(
                output_models.UsePotionMessage(
                    actor_name=self.name,
                    potions_used=0,
                    heal_amount=0,
                    potions_remaining=self.inventory.potions,
                    fully_healed=self.is_fully_healed(),
                    ignore_fully_healed=ignore_fully_healed,
                )
            )
            return Inventory.PotionResult(
                success=False,
                no_potions=False,
                fully_healed=self.is_fully_healed(),
            )
        core_io.send_output(
            output_models.UsePotionMessage(
                actor_name=self.name,
                potions_used=0,
                heal_amount=0,
                potions_remaining=self.inventory.potions,
                fully_healed=self.is_fully_healed(),
                ignore_fully_healed=ignore_fully_healed,
            )
        )
        return Inventory.PotionResult(
            success=False,
            no_potions=True,
            fully_healed=self.is_fully_healed(),
        )

    @staticmethod
    def _get_attack_power(
        specialization: str,
        strength: int,
        intellect: int,
        agility: int,
    ) -> int:
        match specialization:
            case "WARRIOR":  # Str + 1/4 agility
                attack_power = strength + int(agility * 0.25)
                return attack_power * 10
            case "MAGE":  # Int + 1/4 Str
                attack_power = intellect + int(strength * 0.25)
                return attack_power * 10
            case "ROGUE":  # Agl + 1/4 average of str & int
                attack_power = agility + int(((strength + intellect) * 0.5) * 0.25)
                return attack_power * 10
            case _:
                raise ValueError(f"Invalid specialization {specialization}")

    def _get_skill(self) -> str:
        strength_skill = ""
        intellect_skill = ""
        player_skill = ""

        if self.strength in range(1, 4):
            strength_skill = "weak"
        elif self.strength in range(4, 7):
            strength_skill = "fair"
        elif self.strength in range(7, 10):
            strength_skill = "strong"
        elif self.strength == 10:
            strength_skill = "mighty"

        if self.intellect in range(1, 4):
            intellect_skill = "dull"
        elif self.intellect in range(4, 7):
            intellect_skill = "ordinary"
        elif self.intellect in range(7, 10):
            intellect_skill = "smart"
        elif self.intellect == 10:
            intellect_skill = "brilliant"

        player_skill = str(f"{strength_skill}:{intellect_skill}")

        return player_skill

    @staticmethod
    def _get_attack_name(specialization: str) -> str:
        match specialization:
            case "WARRIOR":
                return "Greatsword Cleave"
                # if self.intellect >= 7:
                #    attack = "Arcane Greatsword Cleave"
                # else:
                #    attack = "Greatsword Cleave"

                # min str: 5
                # max str: 10

                # min int: 1
                # max int: 5

                # min agl: 4
                # max agl: 8
            case "MAGE":
                return "Arcane Lightning"
                # if self.strength >= 7:
                #    attack = "Arcane Shockwave"
                # else:
                #    attack = "Arcane Bolt"
                # min str: 1
                # max str: 5

                # min int: 5
                # max int: 10

                # min agl: 4
                # max agl: 8
            case "ROGUE":
                return "Precision Strike"
                # if self.intellect >= 7 and self.strength >= 7:
                #    attack = "Cool Attack"
                # else:
                #    attack = "Precision Dagger Strike"
                # min str: 4
                # max str: 8

                # min int: 4
                # max int: 8

                # min agl: 5
                # max agl: 10
            case _:
                raise ValueError(f"Error Invalid Specialization {specialization}")

    @staticmethod
    def _get_react_action(specialization: str, name: str) -> tuple[str, dict[str, str]]:
        match specialization:
            case "WARRIOR":
                return (
                    "DEFLECT",
                    {
                        "prep_message": f"{name} prepares to deflect against next attack",
                        "success_message": f"{name} successfully deflected the enemy's attack!",
                        "failure_message": f"{name} failed to deflect the attack!",
                    },
                )
            case "MAGE":
                return (
                    "ELUDE",
                    {
                        "prep_message": f"{name} prepares to elude the next attack",
                        "success_message": f"{name} fools the enemy with an illusion!",
                        "failure_message": f"{name} failed to fool the enemy illusion!",
                    },
                )
            case "ROGUE":
                return (
                    "EVADE",
                    {
                        "prep_message": f"{name} prepares to evade the next attack",
                        "success_message": f"{name} deftly evades the enemy's attack!",
                        "failure_message": f"{name} fails to evade the attack!",
                    },
                )
            case _:
                raise ValueError(f"Invalid specialization {specialization}")

    @staticmethod
    def _get_special_attack(specialization: str) -> str:
        match specialization:
            case "WARRIOR":
                return "DISMEMBER"
            case "MAGE":
                return "THUNDERBALL"
            case "ROGUE":
                return "DOUBLE STRIKE"
            case _:
                raise ValueError(f"Invalid specialization {specialization}")
