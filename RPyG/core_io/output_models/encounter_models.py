from dataclasses import dataclass

from RPyG.core_io.output_models.base_models import OutputMessage


@dataclass(kw_only=True, frozen=True, slots=True)
class GenericEncounterMessage(OutputMessage):
    pass


@dataclass(kw_only=True, frozen=True, slots=True)
class EnemyEncouterMessage(OutputMessage):
    enemy_party_name: str
    message: str = ""


@dataclass(kw_only=True, frozen=True, slots=True)
class FleeResultMessage(OutputMessage):
    success: bool
    actor_name: str
    enemy_party_name: str
    message: str = ""


@dataclass(kw_only=True, frozen=True, slots=True)
class MerchantInteractionMessage(OutputMessage):
    @dataclass(kw_only=True, frozen=True, slots=True)
    class MerchantEvent:
        gold_change: int
        success: bool
        item_name: str
        item_count_change: int
        buyer_actor_name: str
        seller_actor_name: str = "Merchant"

    event: MerchantEvent
    message: str = ""


@dataclass(kw_only=True, frozen=True, slots=True)
class MerchantMenuHudDataMessage(OutputMessage):
    actor_name: str
    potion_count: int
    gold_count: int
    message: str = ""
