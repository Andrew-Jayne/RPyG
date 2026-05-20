import copy
import random
from typing import TYPE_CHECKING, cast

from RPyG.constructs.actor.actors.base_actor import Actor
from RPyG.core_io import CoreIO, input_models, output_models
from RPyG.utilities import ensure_type


if TYPE_CHECKING is True:
    from RPyG.constructs.actor import CombatantParty
    from RPyG.constructs.actor.actor_containers import CombatantType
    ## CombatantType is only ever used here so it does not get the full re-export from root


class CombatantActor(Actor):
    health: int
    base_health: int
    attack_name: str
    attack_power: int
    special_attack_name: str
    special_attack_energy: int
    specialization: str
    use_special_attack: bool
    will_react: bool
    is_dismembered: bool
    __slots__: tuple[str, ...] = (
        "health",
        "base_health",
        "attack_name",
        "attack_power",
        "special_attack_name",
        "special_attack_energy",
        "specialization",
        "use_special_attack",
        "will_react",
        "is_dismembered",
    )

    def __init__(
        self,
        name: str,
        strength: int,
        intellect: int,
        agility: int,
        luck: int,
        health: int,
        base_health: int,
        attack_name: str,
        attack_power: int,
        special_attack_name: str,
        specialization: str,
        use_special_attack: bool = False,
        will_react: bool = False,
        is_dismembered: bool = False,
    ) -> None:
        ensure_type(name, str, "name")
        ensure_type(strength, int, "strength")
        ensure_type(intellect, int, "intellect")
        ensure_type(agility, int, "agility")
        ensure_type(luck, int, "luck")
        ensure_type(health, int, "health")
        ensure_type(attack_name, str, "attack_name")
        ensure_type(attack_power, int, "attack_power")
        ensure_type(special_attack_name, str, "special_attack_name")

        if len(name) > 32:
            raise ValueError("Combatant Name cannot exceed 32 characters")
        if health > 9999:
            raise ValueError("Combatant Health cannot exceed 9999")

        Actor.__init__(
            self=self,
            name=name,
            strength=strength,
            intellect=intellect,
            agility=agility,
            luck=luck,
        )

        self.health = health
        self.base_health = base_health

        self.attack_name = attack_name
        self.special_attack_name = special_attack_name
        self.special_attack_energy = 2
        self.attack_power = attack_power
        self.specialization = specialization

        self.use_special_attack = use_special_attack
        self.will_react = will_react
        self.is_dismembered = is_dismembered

    def damage(self, damage_amount: int) -> None:
        ensure_type(damage_amount, int, "damage_amount")
        core_io = CoreIO.get_core_io()

        self.health -= damage_amount
        if self.health == 0:
            self.health = 1
            core_io.send_output(
                output_models.HealthUpdateMessage(
                    actor_name=self.name,
                    magnitude=damage_amount * -1,
                    remaining_health=self.health,
                    evaded_death=True,
                )
            )
            return

        if self.health < 0:
            self.health = 0
            core_io.send_output(
                output_models.HealthUpdateMessage(
                    actor_name=self.name,
                    magnitude=damage_amount * -1,
                    remaining_health=self.health,
                    evaded_death=False,
                )
            )
            return

        core_io.send_output(
            output_models.HealthUpdateMessage(
                actor_name=self.name,
                magnitude=damage_amount * -1,
                remaining_health=self.health,
                evaded_death=False,
            )
        )

    def heal(self, heal_amount: int) -> None:
        ensure_type(heal_amount, int, "heal_amount")
        core_io = CoreIO.get_core_io()

        fully_healed = False
        self.health += heal_amount
        if self.health > self.base_health:
            self.health = self.base_health
            fully_healed = True

        core_io.send_output(
            output_models.HealthUpdateMessage(
                actor_name=self.name,
                magnitude=heal_amount,
                remaining_health=self.health,
                fully_healed=fully_healed,
            )
        )

    def dismember(self) -> None:
        self.is_dismembered = True
        self.attack_power = int(self.attack_power * 0.75)

    def is_fully_healed(self) -> bool:
        return self.health >= self.base_health

    def is_alive(self) -> bool:
        return self.health > 0

    def check_for_critical(self) -> bool:
        return random.randint(1, 100) <= (self.luck + self.agility)

    def attack(self, target_instance: "CombatantActor") -> None:
        from RPyG.constructs.actor import CombatantActor

        core_io = CoreIO.get_core_io()

        ensure_type(target_instance, CombatantActor, "attacker_instance")

        damage_variation = int(self.attack_power * 0.1)
        final_damage = self.attack_power + random.randint(
            -damage_variation,
            damage_variation,
        )
        critical_hit = self.check_for_critical()
        if critical_hit is True:
            final_damage = final_damage * 2

        core_io.send_output(
            output_models.BattleUpdateMessage(
                event=output_models.BattleUpdateMessage.AttackEvent(
                    source_actor_name=self.name,
                    attack_name=self.attack_name,
                    target_actor_name=target_instance.name,
                    magnitude=final_damage,
                    is_critical=critical_hit,
                )
            )
        )
        target_instance.damage(final_damage)

    def react(self) -> bool:
        from RPyG.constructs.actor import PlayableActor

        if isinstance(self, PlayableActor) is True:
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

    def dismember_attack(self, target_instance: "CombatantActor") -> None:
        from RPyG.constructs.actor import CombatantActor, EnemyActor

        core_io = CoreIO.get_core_io()

        ensure_type(target_instance, CombatantActor, "attacker_instance")

        if random.randint(0, 99) in list(range(int(self.luck / 2))):
            if isinstance(target_instance, EnemyActor) is True:
                target_instance = cast(EnemyActor, target_instance)
                if target_instance.is_special is False:
                    core_io.send_output(
                        output_models.BattleUpdateMessage(
                            event=output_models.BattleUpdateMessage.DismemberAttackEvent(
                                source_actor_name=self.name,
                                target_actor_name=target_instance.name,
                                target_decapitated=True,
                            )
                        )
                    )
                    target_instance.health = 0
                    return

        damage_variation = int(self.attack_power * 0.1)
        base_damage = self.attack_power + random.randint(
            -damage_variation, damage_variation
        )
        final_damage = int(base_damage * 0.25)

        critical_hit = self.check_for_critical()
        if critical_hit is True:
            final_damage = final_damage * 2

        core_io.send_output(
            output_models.BattleUpdateMessage(
                event=output_models.BattleUpdateMessage.AttackEvent(
                    source_actor_name=self.name,
                    attack_name=self.attack_name,
                    target_actor_name=target_instance.name,
                    magnitude=final_damage,
                    is_critical=critical_hit,
                )
            )
        )
        core_io.send_output(
            output_models.BattleUpdateMessage(
                event=output_models.BattleUpdateMessage.DismemberAttackEvent(
                    source_actor_name=self.name,
                    target_actor_name=target_instance.name,
                    target_dismembered=True,
                )
            )
        )
        target_instance.damage(final_damage)
        target_instance.dismember()

    def aoe_attack(
        self,
        target_party_instance: "CombatantParty[CombatantType]",
    ) -> None:
        from RPyG.constructs.actor import CombatantParty

        core_io = CoreIO.get_core_io()

        ensure_type(target_party_instance, CombatantParty, "target_party_instance")

        # set damage
        damage_variation = int(self.attack_power * 0.1)
        base_damage = (
            int(self.attack_power + random.randint(-damage_variation, damage_variation))
            * 1.5
        )
        per_target_damage = int(base_damage / len(target_party_instance.members))

        critical_hit = self.check_for_critical()
        if critical_hit is True:
            per_target_damage = per_target_damage * 2
        target_names: list[str] = []
        for instance in target_party_instance.members:
            target_names.append(instance.name)
        self_damage_amount = 0
        damage_self = self.intellect <= random.randint(0, 12)
        if damage_self is True:
            self_damage_amount = int(per_target_damage * 0.125)

        core_io.send_output(
            output_models.BattleUpdateMessage(
                event=output_models.BattleUpdateMessage.AoeAttackEvent(
                    attack_name=self.special_attack_name,
                    source_actor_name=self.name,
                    target_actor_names=target_names,
                    per_target_damage=per_target_damage,
                    is_critical=critical_hit,
                    self_damage=damage_self,
                    self_damage_magnitude=self_damage_amount,
                )
            )
        )

        for target_instance in target_party_instance.members:
            core_io.send_output(
                output_models.BattleUpdateMessage(
                    event=output_models.BattleUpdateMessage.AttackEvent(
                        source_actor_name=self.name,
                        attack_name=self.attack_name,
                        target_actor_name=target_instance.name,
                        magnitude=per_target_damage,
                        is_critical=critical_hit,
                    )
                )
            )
            target_instance.damage(per_target_damage)

        if damage_self is True:
            self.damage(self_damage_amount)

    def double_attack(
        self,
        target_party_instance: "CombatantParty[CombatantType]",
    ) -> None:
        from RPyG.constructs.actor import CombatantParty

        core_io = CoreIO.get_core_io()

        ensure_type(target_party_instance, CombatantParty, "target_party_instance")

        # set primary target
        primary_target_index = self.select_combat_target(target_party_instance)
        primary_instance: CombatantActor = target_party_instance.members[
            primary_target_index
        ]

        # set secondary target
        secondary_target_index = self.select_combat_target(target_party_instance)
        secondary_instance: CombatantActor = target_party_instance.members[
            secondary_target_index
        ]
        self_damage_amount = 0
        damage_self = (self.luck + self.agility) < random.randint(0, 25)
        if damage_self is True:
            self_damage_amount = int(secondary_instance.attack_power * 0.5)
        is_critical = self.check_for_critical()
        secondary_target_damage = int(self.attack_power / 2)
        base_damage = copy.deepcopy(self.attack_power)

        core_io.send_output(
            output_models.BattleUpdateMessage(
                event=output_models.BattleUpdateMessage.DoubleAttackEvent(
                    attack_name=self.special_attack_name,
                    source_actor_name=self.name,
                    primary_target_name=primary_instance.name,
                    secondary_target_name=secondary_instance.name,
                    is_critical=is_critical,
                    self_damage=damage_self,
                    self_damage_magnitude=self_damage_amount,
                )
            )
        )

        self.attack(primary_instance)

        # Check if Target Died
        if primary_instance.health == 0:
            target_party_instance.lose_member(primary_instance)

        # Make Sure a Living target is chosen and party is not all dead
        # This prevents a softlock if you kill the last target on attack 1
        if (
            len(target_party_instance.members) != 0
            and secondary_instance in target_party_instance.members
        ):
            # reduce ATK by 50% for attack 2, then restore
            self.attack_power = secondary_target_damage
            self.attack(secondary_instance)
            self.attack_power = base_damage

            # Check if Target Died
            if secondary_instance.health == 0:
                target_party_instance.lose_member(secondary_instance)
                return

        if damage_self is True:
            self.damage(self_damage_amount)

    def special_attack(
        self,
        target_party_instance: "CombatantParty[CombatantType]",
    ) -> None:
        from RPyG.constructs.actor import CombatantParty
        from RPyG.core_io import CoreIO

        core_io = CoreIO.get_core_io()

        ensure_type(target_party_instance, CombatantParty, "target_party_instance")

        match self.specialization:
            case "WARRIOR":
                target_index = int(self.select_combat_target(target_party_instance))
                target_instance: CombatantActor = target_party_instance.members[
                    target_index
                ]
                if target_instance.is_dismembered is True:
                    core_io.send_output(
                        output_models.BattleUpdateMessage(
                            event=output_models.BattleUpdateMessage.InvalidTargetEvent()
                        )
                    )
                    self.attack(target_instance)
                else:
                    self.dismember_attack(target_instance=target_instance)
            case "MAGE":
                self.aoe_attack(target_party_instance)
            case "ROGUE":
                self.double_attack(target_party_instance)
            case _:
                raise ValueError(f"Invalid specialization {self.specialization}")

    def select_combat_target(
        self, target_party_instance: "CombatantParty[CombatantType]"
    ) -> int:
        """
        Takes a full party instance, and returns the index of the target member in the members array/list as an int
        """
        from RPyG.constructs.actor import CombatantParty, EnemyParty, PlayableActor
        from RPyG.core_io import CoreIO

        core_io = CoreIO.get_core_io()

        ensure_type(target_party_instance, CombatantParty, "target_party_instance")
        if (
            isinstance(self, PlayableActor) is True
            and isinstance(target_party_instance, EnemyParty) is True
        ):
            target_messages: list[str] = ["Which enemy will you attack?"]
            target_indexes: list[str] = []
            for index, member in enumerate(target_party_instance.members):
                member: CombatantActor
                target_messages.append(f"{index} {member.name}:{member.health}")
                target_indexes.append(str(index))

            core_io.request_int_input(
                input_models.UserPromptRequest(
                    prompts=target_messages,
                    options=target_indexes,
                )
            )
            return core_io.receive_int_input()
        else:
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
                    raise ValueError(
                        "Big Problem in Select_Target, Go buy a lotto ticket"
                    )
