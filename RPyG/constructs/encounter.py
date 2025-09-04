from enum import Enum

from RPyG.utilites import ensure_type


class EncounterType(Enum):
    REST = "REST"
    LOOT = "LOOT"
    # None Encounters are used as chain ends, this should be done better
    NONE = "NONE"
    MYSTERY = "MYSTERY"
    SPECAIAL = "SPECIAL"


class EncounterTarget(Enum):
    ALL = "ALL"
    RANDOM = "RANDOM"


class ActorAction(Enum):
    HEAL = "HEAL"
    DAMAGE = "DAMAGE"
    GAIN_GOLD = "GAIN_GOLD"
    LOSE_GOLD = "LOSE_GOLD"
    GAIN_POTION = "GAIN_POTION"
    LOSE_POTION = "LOSE_POTION"


class SpecialAction(Enum):
    AT_MERCHANT = "AT_MERCHANT"


class Encounter:
    __slots__ = (
        "encounter_type",
        "targets",
        "magnitude",
        "message",
        "pre_message",
        "post_message",
        "actor_action",
        "special_action",
        "additional_events",
    )
    encounter_type: EncounterType
    targets: EncounterTarget
    magnitude: int
    message: str | None
    pre_message: str | None
    post_message: str | None
    actor_action: ActorAction
    special_action: SpecialAction | None
    additional_events: list[str] | None

    def __init__(
        self,
        kind: str,
        encounter_type: EncounterType,
        actor_action: ActorAction,
        targets: EncounterTarget,
        magnitude: int,
        message: str | None = None,
        pre_message: str | None = None,
        post_message: str | None = None,
        special_action: SpecialAction | None = None,
        additional_events: list[str] | None = None,
    ) -> None:
        ensure_type(encounter_type, str, "encounter_type")
        ensure_type(actor_action, str, "actor_action")
        ensure_type(targets, str, "targets")
        ensure_type(magnitude, int, "magnitude")
        if message is not None:
            ensure_type(message, str, "message")
        if pre_message is not None:
            ensure_type(pre_message, str, "pre_message")
        if post_message is not None:
            ensure_type(post_message, str, "post_message")
        if special_action is not None:
            ensure_type(special_action, str, "special_action")
        if additional_events is not None:
            ensure_type(additional_events, list, "additional_events")
            for additional_event_item in additional_events:
                ensure_type(additional_event_item, str, "additional_event_item")

        self.encounter_type = EncounterType(encounter_type)
        self.actor_action = ActorAction(actor_action)
        self.targets = EncounterTarget(targets)
        self.magnitude = magnitude

        self.message = message
        self.pre_message = pre_message
        self.post_message = post_message

        if special_action is not None:
            self.special_action = SpecialAction(special_action)
        else:
            self.special_action = None
        self.additional_events = additional_events

    def validate(self) -> bool:
        return True
