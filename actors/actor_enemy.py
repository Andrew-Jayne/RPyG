from actors.actor_combatant import Combatant, CombatantParty
from utilites.utilities import ensure_type


class Enemy(Combatant):
    is_special: bool

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
        self.is_special = enemy_attributes["is_special"]

        Combatant.__init__(
            self,
            name=enemy_attributes["name"],
            strength=enemy_attributes["strength"],
            intellect=enemy_attributes["intellect"],
            agility=enemy_attributes["agility"],
            luck=enemy_attributes["luck"],
            health=enemy_attributes["health"],
            attack_name=enemy_attributes["attack_name"],
            attack_power=Enemy._set_enemy_attack_power(
                enemy_attributes["strength"],
                enemy_attributes["intellect"],
            ),
            special_attack_name=None,
        )

    def _set_enemy_attack_power(strength: int, intellect: int) -> int:
        if strength >= 6 and intellect >= 6:
            attack_power = strength + intellect
        elif strength > intellect:
            attack_power = strength
        elif strength < intellect:
            attack_power = intellect
        else:
            attack_power = int((strength + intellect) / 2)

        return attack_power * 10


class EnemyParty(CombatantParty):
    members: list[Enemy]
    dead_members: list[Enemy]
    loot: object

    def __init__(
        self,
        name: str,
        members: list[Enemy],
    ) -> None:
        ensure_type(name, str, "name")
        ensure_type(members, list, "members")
        for party_member in members:
            ensure_type(party_member, Enemy, "party_member")

        CombatantParty.__init__(
            self,
            name=name,
            members=members,
        )

        self.loot = None
