import random
from typing import Generic, TypeVar, TYPE_CHECKING, cast

from actors.actor_base import Actor, Party
from utilites import ensure_type

if TYPE_CHECKING:
    from actors import PlayerParty, EnemyParty


class Combatant(Actor):
    name: str
    strength: int
    intellect: int
    agility: int
    luck: int
    health: int
    attack_name: str
    attack_power: int
    special_attack_name: str | None
    specialization: str

    def __init__(
        self,
        name: str,
        strength: int,
        intellect: int,
        agility: int,
        luck: int,
        health: int,
        attack_name: str,
        attack_power: int,
        special_attack_name: str | None,
        specialization: str,
    ) -> None:
        ensure_type(name, str, "name")
        ensure_type(strength, int, "strength")
        ensure_type(intellect, int, "intellect")
        ensure_type(agility, int, "agility")
        ensure_type(luck, int, "luck")
        ensure_type(health, int, "health")
        ensure_type(attack_name, str, "attack_name")
        ensure_type(attack_power, int, "attack_power")
        if special_attack_name is not None:
            ensure_type(special_attack_name, str, 'special_attack_name')
        Actor.__init__(
            self=self,
            name=name,
            strength=strength,
            intellect=intellect,
            agility=agility,
            luck=luck,
        )

        self.health = health
        self.base_health = health

        self.attack_name = attack_name
        self.special_attack_name = special_attack_name
        self.special_attack_energy = 2
        self.attack_power = attack_power
        self.specialization = specialization

        self.use_special_attack = False
        self.will_react = False
        self.is_dismembered = False

    def damage(self, damage_amount: int) -> None:
        ensure_type(damage_amount, int, "damage_amount")

        from message.message import Message

        self.health -= damage_amount
        if self.health == 0:
            self.health = 1
            Message.display_message(f"{self.name} has Narrowly Evaded Death!", 1)
        elif self.health < 0:
            self.health = 0
        Message.display_message(f"{self.name} has {self.health} Health Remaining", 2)

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
        return self.health > 0

    def check_for_critical(self) -> bool:
        return random.randint(1, 100) <= (self.luck + self.agility)

    def attack(self, target_instance: "Combatant") -> None:
        from actors import Combatant
        from message.message import Message

        ensure_type(target_instance, Combatant, "attacker_instance")

        damage_variation = int(self.attack_power * 0.1)
        final_damage = self.attack_power + random.randint(
            -damage_variation,
            damage_variation,
        )

        if self.check_for_critical() is True:
            Message.actor_critical_attack_message(self, final_damage)
            target_instance.damage(final_damage * 2)
        else:
            Message.actor_attack_message(self, final_damage)
            target_instance.damage(final_damage)

    def react(self) -> bool:
        from actors import PlayableActor

        if isinstance(self, PlayableActor):
            match self.specialization:
                case "WARRIOR":
                    return random.randint(1, 30) <= (self.luck + self.strength)
                case "MAGE":
                    return random.randint(1, 30) <= (self.luck + self.intellect)
                case "ROGUE":
                    return random.randint(1, 30) <= (self.luck + self.agility)
                case _:
                    raise ValueError(f"Invalid Specialization {self.specialization}")
        else:
            return random.randint(1, 30) <= (self.luck + self.agility)

    def dismember_attack(self, target_instance: "Combatant") -> None:
        from actors import Combatant, Enemy
        from message.message import Message

        ensure_type(target_instance, Combatant, "attacker_instance")

        if random.randint(0, 99) in list(range(int(self.luck / 2))):
            if (
                isinstance(target_instance, Enemy)
                and target_instance.is_special is False
            ):
                decapitate_message = f"{self.name} decapitates {target_instance.name} killing them instantly"
                Message.display_message(decapitate_message, 1)
                target_instance.health = 0

        damage_variation = int(self.attack_power * 0.1)
        base_damage = self.attack_power + random.randint(
            -damage_variation, damage_variation
        )
        final_damage = int(base_damage * 0.25)
        dismember_message = f"""
    {self.name} dismembers {target_instance.name} inflicting {final_damage} damage
    {target_instance.name}'s attack power has been reduced by 25%
    """
        dismember_critical_message = f"""
    {self.name} got a critical hit!
    {self.name} dismembers {target_instance.name} inflicting {final_damage * 2} damage
    {target_instance.name}'s attack power has been reduced by 25%
    """

        if self.check_for_critical() is True:
            target_instance.dismember()
            target_instance.damage(final_damage * 2)
            Message.display_message(dismember_critical_message, 2)
        else:
            target_instance.damage(final_damage)
            target_instance.dismember()
            Message.display_message(dismember_message, 2)

    def aoe_attack(self, target_party_instance: "PlayerParty | EnemyParty") -> None:
        from actors import CombatantParty
        from message.message import Message

        ensure_type(target_party_instance, CombatantParty, "target_party_instance")

        # set damage
        damage_variation = int(self.attack_power * 0.1)
        base_damage = int(
            self.attack_power
            + random.randint(-damage_variation, damage_variation) * 1.5
        )
        per_target_damage = int(base_damage / len(target_party_instance.members))

        aoe_attack_message = f"{self.name} attacks with {self.special_attack_name} dealing {per_target_damage} damage to all enemies"
        aoe_critical_attack_message = f"""
    {self.name} attacks with {self.special_attack_name} dealing {per_target_damage * 2} damage to all enemies
    {self.name} dealt critical hits to all enemies!
        """

        if self.check_for_critical() is True:
            Message.display_message(aoe_critical_attack_message, 1)
            for target_instance in target_party_instance.members:
                target_instance.damage(per_target_damage * 2)
        else:
            Message.display_message(aoe_attack_message, 1)
            for target_instance in target_party_instance.members:
                target_instance.damage(per_target_damage)

        if self.intellect <= random.randint(0, 12):
            self_damage_amount = int(per_target_damage * 0.125)
            self.damage(self_damage_amount)
            overwhelm_message = f"{self.name} is overwhelmed by the power of {self.special_attack_name} and takes {self_damage_amount} damage"
            Message.display_message(overwhelm_message, 1)

    def double_attack(self, target_party_instance: "PlayerParty | EnemyParty") -> None:
        from actors import CombatantParty
        from message.message import Message
        from actors import PlayerParty, EnemyParty, Enemy, PlayableActor

        ensure_type(target_party_instance, CombatantParty, "target_party_instance")

        # set primary target
        primary_target_index = self.select_combat_target(target_party_instance)
        primary_instance: Combatant = target_party_instance.members[
            primary_target_index
        ]

        # set secondary target
        secondary_target_index = self.select_combat_target(target_party_instance)
        secondary_instance = target_party_instance.members[secondary_target_index]

        # Damage Primary Target
        damage_variation = int(self.attack_power * 0.1)
        final_damage = self.attack_power + random.randint(
            -damage_variation, damage_variation
        )

        if self.check_for_critical() is True:
            Message.actor_critical_attack_message(self, final_damage)
            primary_instance.damage(final_damage * 2)
        else:
            Message.actor_attack_message(self, final_damage)
            primary_instance.damage(final_damage)

        # Check if Target Died
        if primary_instance.health == 0:
            Message.defeated_message(primary_instance.name)
            if isinstance(target_party_instance, PlayerParty) is True:
                player_party_instance = cast(PlayerParty, target_party_instance)
                primary_actor = cast(PlayableActor, primary_instance)
                player_party_instance.lose_member(primary_actor)

            if isinstance(target_party_instance, EnemyParty) is True:
                enemy_party_instance = cast(EnemyParty, target_party_instance)
                primary_enemy = cast(Enemy, primary_instance)
                enemy_party_instance.lose_member(primary_enemy)

        # Make Sure a Living target is chosen
        # This prevents a softlock, if you kill the last target on attack 1
        if len(target_party_instance.members) != 0:
            # Damage Secondary Target
            reduced_damage = int(final_damage * 0.5)

            if secondary_instance not in target_party_instance.members:
                while secondary_instance not in target_party_instance.members:
                    Message.display_message("Select a Living Target", 1)
                    secondary_target_index = self.select_combat_target(
                        target_party_instance
                    )
                    secondary_instance = target_party_instance.members[
                        secondary_target_index
                    ]

            if self.check_for_critical() is True:
                Message.actor_critical_attack_message(self, reduced_damage)
                secondary_instance.damage(reduced_damage * 2)
            else:
                Message.actor_attack_message(self, reduced_damage)
                secondary_instance.damage(reduced_damage)

            # Check if Target Died
            if secondary_instance.health == 0:
                Message.defeated_message(secondary_instance.name)
                if isinstance(target_party_instance, PlayerParty) is True:
                    player_party_instance = cast(PlayerParty, target_party_instance)
                    secondary_actor = cast(PlayableActor, secondary_instance)
                    player_party_instance.lose_member(secondary_actor)

                if isinstance(target_party_instance, EnemyParty) is True:
                    enemy_party_instance = cast(EnemyParty, target_party_instance)
                    secondary_enemy = cast(Enemy, secondary_instance)
                    enemy_party_instance.lose_member(secondary_enemy)

            # luck + agl in 25 to get caught and take 50% target damage from target 2
            if (self.luck + self.agility) < random.randint(0, 25):
                self.damage(int(secondary_instance.attack_power * 0.5))
                caught_attack_message = f"{self.name} fails fails to evade an attack from {secondary_instance.name} and takes {int(secondary_instance.attack_power * 0.5)} damage"
                Message.display_message(caught_attack_message, 2)

    def special_attack(self, target_party_instance: "PlayerParty | EnemyParty") -> None:
        from actors import CombatantParty
        from message.message import Message

        ensure_type(target_party_instance, CombatantParty, "target_party_instance")

        match self.specialization:
            case "WARRIOR":
                target_index = int(self.select_combat_target(target_party_instance))
                target_instance = target_party_instance.members[target_index]
                if target_instance.is_dismembered is True:
                    dumb_check = 0
                    while target_instance.is_dismembered is True:
                        dumb_check += 1
                        Message.display_message(
                            f"{target_instance.name} has been dismembered already", 1
                        )
                        # message that enemy has been dismembered
                        target_index = self.select_combat_target(target_party_instance)
                        target_instance = target_party_instance.members[target_index]
                        # might be a case where you try to attack the last enemy with dismemeber
                        # but they have been dismembered, so just skip to attack normal
                        if dumb_check > 10 or len(target_party_instance.members) == 1:
                            # dumb message
                            self.attack(target_party_instance.members[0])
                self.dismember_attack(target_instance=target_instance)
            case "MAGE":
                self.aoe_attack(target_party_instance)
            case "ROGUE":
                self.double_attack(target_party_instance)
            case _:
                raise ValueError(f"Invalid specialization {self.specialization}")

    def select_combat_target(
        self, target_party_instance: "PlayerParty | EnemyParty"
    ) -> int:
        """
        Takes a full party instance, and returns the index of the target member in the members array/list as an int
        """
        from actors import EnemyParty, PlayableActor

        from interaction.interaction import Interaction

        ensure_type(target_party_instance, CombatantParty, "target_party_instance")

        if (
            isinstance(self, PlayableActor) is True
            and isinstance(target_party_instance, EnemyParty) is True
        ):
            enemy_party_instance: EnemyParty = cast(EnemyParty, target_party_instance)
            return Interaction.choose_combat_target(enemy_party_instance)

        target_party_members = target_party_instance.members
        method_id = random.choice(["MAX_ATK", "MIN_HP", "RANDOM"])
        match method_id:
            case "MAX_ATK":
                target_attributes_list: list[tuple[int, int]]
                target_attributes_list = []

                for index, member in enumerate(target_party_members):
                    target_attributes: tuple[int, int]
                    target_attributes = (index, member.attack_power)

                    target_attributes_list.append(target_attributes)
                sorted_target_attributes_list = sorted(
                    target_attributes_list, key=lambda x: x[1], reverse=True
                )
                return sorted_target_attributes_list[0][0]

            case "MIN_HP":
                target_attributes_list = []
                for index, member in enumerate(target_party_members):
                    target_attributes = (index, member.health)
                    target_attributes_list.append(target_attributes)
                sorted_target_attributes_list = sorted(
                    target_attributes_list, key=lambda x: x[1]
                )
                return sorted_target_attributes_list[0][0]

            case "RANDOM":
                return random.randint(0, (len(target_party_members) - 1))
            case _:
                raise ValueError("Big Problem in Select_Target, Go buy a lotto ticket")


CombatantType = TypeVar("CombatantType", bound=Combatant)


class CombatantParty(Party[CombatantType], Generic[CombatantType]):
    name: str
    members: list[CombatantType]
    dead_members: list[CombatantType]

    def __init__(
        self,
        name: str,
        members: list[CombatantType],
    ) -> None:
        ensure_type(name, str, "name")
        ensure_type(members, list, "members")

        for party_member in members:
            ensure_type(party_member, Combatant, "party_member")

        ## super() Must be used because of typing and use of generics
        super().__init__(
            members=members,
        )
        self.name = name
        self.dead_members = []

    def lose_member(self, member: CombatantType) -> None:
        self.dead_members.append(member)
        self.members.remove(member)

    def gain_member(self, member: CombatantType) -> None:
        self.members.append(member)
