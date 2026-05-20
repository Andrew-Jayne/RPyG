from dataclasses import dataclass

from RPyG.core_io.output_models.base_models import OutputMessage


@dataclass(kw_only=True, frozen=True, slots=True)
class UsePotionMessage(OutputMessage):
    message: str = ""
    actor_name: str
    potions_used: int
    heal_amount: int
    potions_remaining: int
    fully_healed: bool
    ignore_fully_healed: bool


@dataclass(kw_only=True, frozen=True, slots=True)
class HealthUpdateMessage(OutputMessage):
    actor_name: str
    magnitude: int
    remaining_health: int
    message: str = ""
    evaded_death: bool = False
    fully_healed: bool = False


@dataclass(kw_only=True, frozen=True, slots=True)
class ActorDefeatedMessage(OutputMessage):
    actor_name: str
    message: str = ""


@dataclass(kw_only=True, frozen=True, slots=True)
class UseGoldMessage(OutputMessage):
    @dataclass(kw_only=True, frozen=True, slots=True)
    class GoldUsedEvent:
        success: bool
        final_amount: int

    @dataclass(kw_only=True, frozen=True, slots=True)
    class NoGoldEvent(GoldUsedEvent):
        success: bool = False
        final_amount: int = 0

    @dataclass(kw_only=True, frozen=True, slots=True)
    class InsufficientGoldEvent(GoldUsedEvent):
        success: bool = False

    event: GoldUsedEvent
    actor_name: str
    message: str = ""
