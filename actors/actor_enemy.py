from actors.actor import Actor
from actors.actor_combatant import Combatant
from utilites.utilities import ensure_type


class Enemy(Actor, Combatant):
    def __init__(self, enemy_attributes: dict) -> None:
        ensure_type(enemy_attributes, dict, "enemy_attributes")
        ensure_type(enemy_attributes["name"], str, "enemy_attributes['name']")
        ensure_type(enemy_attributes["health"], int, "enemy_attributes['health']")
        ensure_type(enemy_attributes["strength"], int, "enemy_attributes['strength']")
        ensure_type(enemy_attributes["intellect"], int, "enemy_attributes['intellect']")
        ensure_type(enemy_attributes["agility"], int, "enemy_attributes['agility']")
        ensure_type(enemy_attributes["luck"], int, "enemy_attributes['luck']")
        ensure_type(
            enemy_attributes["attack_name"], str, "enemy_attributes['attack_name']"
        )
        ensure_type(
            enemy_attributes["is_special"], bool, "enemy_attributes['is_special']"
        )

        name = enemy_attributes["name"]
        health = enemy_attributes["health"]
        strength = enemy_attributes["strength"]
        intellect = enemy_attributes["intellect"]
        agility = enemy_attributes["agility"]
        luck = enemy_attributes["luck"]
        attack_name = enemy_attributes["attack_name"]
        is_special = enemy_attributes["is_special"]

        attack_power = __class__.__set_enemy_attack_power(strength, intellect)

        ## Init Inherited Classes
        Actor.__init__(
            self,
            name=name,
            strength=strength,
            intellect=intellect,
            agility=agility,
            luck=luck,
        )
        Combatant.__init__(
            self,
            health=health,
            attack_name=attack_name,
            attack_power=attack_power,
            special_attack_name=None,
        )

    def __set_enemy_attack_power(strength: int, intellect: int) -> int:
        if strength >= 6 and intellect >= 6:
            attack_power = strength + intellect
        elif strength > intellect:
            attack_power = strength
        elif strength < intellect:
            attack_power = intellect
        else:
            attack_power = int((strength + intellect) / 2)

        return attack_power * 10
