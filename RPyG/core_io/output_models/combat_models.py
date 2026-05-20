from dataclasses import dataclass

from RPyG.core_io.output_models.base_models import OutputMessage


@dataclass(kw_only=True, frozen=True, slots=True)
class BattleHudData(OutputMessage):
    """
    Transfers a full representation of the combat state to the interface
    the interface may account and display changes to these in any way
    """

    @dataclass(kw_only=True, frozen=True, slots=True)
    class MemberStats:
        name: str
        health: int
        alive: bool

    @dataclass(kw_only=True, frozen=True, slots=True)
    class PartyStats:
        name: str
        member_stats: list[BattleHudData.MemberStats]

    message: str = ""
    player_party_data: PartyStats
    enemy_party_data: PartyStats


@dataclass(kw_only=True, frozen=True, slots=True)
class BattleUpdateMessage(OutputMessage):
    @dataclass(kw_only=True, frozen=True, slots=True)
    class BattleEvent:
        message: str

    @dataclass(kw_only=True, frozen=True, slots=True)
    class AttackEvent(BattleEvent):
        attack_name: str
        magnitude: int
        is_critical: bool
        source_actor_name: str
        target_actor_name: str
        message: str = ""

    @dataclass(kw_only=True, frozen=True, slots=True)
    class AoeAttackEvent(BattleEvent):
        attack_name: str
        source_actor_name: str
        target_actor_names: list[str]
        per_target_damage: int
        is_critical: bool
        self_damage: bool
        self_damage_magnitude: int
        message: str = ""

    @dataclass(kw_only=True, frozen=True, slots=True)
    class DoubleAttackEvent(BattleEvent):
        attack_name: str
        source_actor_name: str
        primary_target_name: str
        secondary_target_name: str
        is_critical: bool
        self_damage: bool
        self_damage_magnitude: int
        message: str = ""

    @dataclass(kw_only=True, frozen=True, slots=True)
    class DismemberAttackEvent(BattleEvent):
        source_actor_name: str
        target_actor_name: str
        target_dismembered: bool = False
        target_decapitated: bool = False
        message: str = ""

    @dataclass(kw_only=True, frozen=True, slots=True)
    class ReactEvent(BattleEvent):
        actor_name: str
        success: bool
        message: str = ""

    @dataclass(kw_only=True, frozen=True, slots=True)
    class PrepareEvent(BattleEvent):
        actor_name: str
        message: str = ""

    @dataclass(kw_only=True, frozen=True, slots=True)
    class ActorDefeatedEvent(BattleEvent):
        actor_name: str
        message: str = ""

    @dataclass(kw_only=True, frozen=True, slots=True)
    class NotEnoughEnergyEvent(BattleEvent):
        current_energy: int
        energy_cost: int
        message: str = ""

    @dataclass(kw_only=True, frozen=True, slots=True)
    class InvalidTargetEvent(BattleEvent):
        target_invalid: bool = True
        message: str = ""

    message: str = ""
    event: BattleEvent


@dataclass(kw_only=True, frozen=True, slots=True)
class BattleStartMessage(OutputMessage):
    message: str = ""
    in_combat: bool = True


@dataclass(kw_only=True, frozen=True, slots=True)
class BattleEndMessage(OutputMessage):
    message: str = ""
    player_victory: bool
    in_combat: bool = False
