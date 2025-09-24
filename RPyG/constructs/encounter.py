import math
import random
from enum import Enum

from RPyG.actors import PlayableActor, PlayerParty
from RPyG.constructs import (
    ActorAction,
    Encounter,
    EncounterTarget,
    EncounterType,
    SpecialAction,
)
from RPyG.content import ContentLibrary
from RPyG.core_io import CoreIO
from RPyG.core_io.io_models import OutputMessage, UserPromptRequest
from RPyG.utilites import ensure_type


class EncounterType(Enum):
    REST = "REST"
    LOOT = "LOOT"
    # None Encounters are used as chain ends, this should be done better
    NONE = "NONE"
    MYSTERY = "MYSTERY"
    SPECIAL = "SPECIAL"


class EncounterTarget(Enum):
    ALL = "ALL"
    RANDOM = "RANDOM"


class SpecialAction(Enum):
    AT_MERCHANT = "AT_MERCHANT"


class Encounter:
    __slots__ = (
        "encounter_type",
        "targets",
        "magnitude",
        "message",
        "success_choice",
        "repeat_choice",
        "failure_choice",
        "pre_message",
        "post_message",
        "actor_action",
        "special_action",
        "additional_events",
    )
    encounter_type: EncounterType
    targets: EncounterTarget
    magnitude: int | None
    success_choice: str | None
    repeat_choice: str | None
    failure_choice: str | None
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
        magnitude: int | None = None,
        success_choice: str | None = None,
        repeat_choice: str | None = None,
        failure_choice: str | None = None,
        message: str | None = None,
        pre_message: str | None = None,
        post_message: str | None = None,
        special_action: SpecialAction | None = None,
        additional_events: list[str] | None = None,
    ) -> None:
        ensure_type(encounter_type, str, "encounter_type")
        ensure_type(actor_action, str, "actor_action")
        ensure_type(targets, str, "targets")
        if magnitude is not None:
            ensure_type(magnitude, int, "magnitude")
        if success_choice is not None:
            ensure_type(success_choice, str, "success_choice")
        if repeat_choice is not None:
            ensure_type(repeat_choice, str, "repeat_choice")
        if failure_choice is not None:
            ensure_type(failure_choice, str, "failure_choice")
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

    def set_encounter_targets(
        self,
        player_party_instance: PlayerParty,
    ) -> list[PlayableActor]:
        ensure_type(player_party_instance, PlayerParty, "player_party_instance")

        match self.targets:
            case EncounterTarget.ALL:
                return player_party_instance.members
            case EncounterTarget.RANDOM:
                return [random.choice(player_party_instance.members)]
            case _:
                raise ValueError(f"invalid target: {self.targets}")

    @staticmethod
    def find_encounter_by_id(target_item_id: str) -> Encounter:
        ensure_type(target_item_id, str, "target_item_id")
        content_library: ContentLibrary = ContentLibrary.get_library()

        # Directly access the event by its ID
        found_item = content_library.encounters.get(target_item_id, None)
        if found_item is None:
            raise FileNotFoundError(
                f"Error: Unable to find an event with the ID {target_item_id}"
            )
        return found_item

    def execute_actor_action(self, target_instance_list: list[PlayableActor]) -> None:
        ensure_type(target_instance_list, list, "target_instance_list")
        for actor in target_instance_list:
            ensure_type(actor, PlayableActor, "actor")
        core_io = CoreIO.get_core_io()

        if self.magnitude is not None:  ## yikes, need some better sorting here
            magnitude = int(self.magnitude / len(target_instance_list))
            if self.message is not None:
                core_io.send_output(OutputMessage(self.message))

            for target in target_instance_list:
                match self.actor_action:
                    case ActorAction.DAMAGE:
                        target.damage(magnitude)
                    case ActorAction.HEAL:
                        target.heal(magnitude)
                    case ActorAction.GAIN_GOLD:
                        target.inventory.gain_gold(magnitude)
                    case ActorAction.LOSE_GOLD:
                        target.inventory.lose_gold(magnitude)
                    case ActorAction.GAIN_POTION:
                        target.inventory.gain_potion(magnitude)
                    case ActorAction.LOSE_POTION:
                        target.inventory.lose_potion(magnitude)
                    case _:
                        raise ValueError(
                            f"Error Invalid Method Call: {self.actor_action}"
                        )

    def execute_special_action(self, player_party_instance: PlayerParty):
        ensure_type(player_party_instance, PlayerParty, "player_party_instance")
        core_io = CoreIO.get_core_io()
        match self.special_action:
            case SpecialAction.AT_MERCHANT:
                player_choice = None
                merchant_options = ["BUY", "LEAVE", "BUY MAX"]

                for player_instance in player_party_instance.members:
                    merchant_messages = [
                        f"{player_instance.name}",
                        f"Gold: {player_instance.inventory.gold}",
                        f"Potions: {player_instance.inventory.potions}",
                        "",
                        "Choose an Action:",
                    ]

                    while player_choice != "LEAVE":
                        core_io.request_input(
                            UserPromptRequest(
                                options=merchant_options,
                                prompts=merchant_messages,
                            )
                        )
                        player_choice = core_io.receive_input()
                        core_io.send_output(
                            OutputMessage(
                                f"{player_instance.name} has {player_instance.inventory.potions} potions & {player_instance.inventory.gold} gold"
                            )
                        )
                        match player_choice:
                            case "BUY":
                                if player_instance.inventory.spend_gold(25) is True:
                                    player_instance.inventory.gain_potion(1)
                                    core_io.send_output(
                                        OutputMessage(
                                            f"{player_instance.name} purchases a potion. They now have {player_instance.inventory.potions} & {player_instance.inventory.gold} gold",
                                        )
                                    )
                                else:
                                    core_io.send_output(
                                        OutputMessage(
                                            f"{player_instance.name} does not have enough Gold to purchase more potions",
                                        )
                                    )
                                    player_choice = "LEAVE"
                            case "BUY MAX":
                                # Using floor to make sure you can't buy 10 potions with 245 gold
                                rounds = math.floor(player_instance.inventory.gold / 25)
                                player_instance.inventory.spend_gold((rounds * 25))
                                player_instance.inventory.gain_potion(rounds)
                                player_choice = "LEAVE"
                            case "LEAVE":
                                player_choice = "LEAVE"
                            case _:
                                player_choice = "LEAVE"
            case _:
                raise ValueError(f"error invalid special_action: {self.special_action}")

    ### wonky flow for event cascades, I don't love this
    def run_extra_actions(self, player_party_instance: PlayerParty) -> None:
        ensure_type(player_party_instance, PlayerParty, "player_party_instance")
        # Run extra Actions if they exist
        if self.additional_events is not None:
            for event_id in self.additional_events:
                new_event: Encounter = self.find_encounter_by_id(event_id)
                targets = new_event.set_encounter_targets(player_party_instance)
                new_event.execute_actor_action(targets)

        # Run Special Actions if they exist
        if self.special_action is not None:
            self.execute_special_action(player_party_instance)

    def run(self, player_party_instance: PlayerParty) -> None:
        ensure_type(player_party_instance, PlayerParty, "player_party_instance")
        content_library: ContentLibrary = ContentLibrary.get_library()
        core_io = CoreIO.get_core_io()

        current_event = random.choice(list(content_library.encounters.values()))

        targets = self.set_encounter_targets(player_party_instance)

        match current_event.encounter_type:
            case EncounterType.REST:
                if current_event.pre_message is not None:
                    core_io.send_output(OutputMessage(current_event.pre_message))

                core_io.request_input(
                    UserPromptRequest(
                        prompts=["What do you do?:"],
                        options=["OPEN", "LEAVE"],
                    )
                )
                action = core_io.receive_input()
                match action:
                    case "OPEN":
                        self.execute_actor_action(targets)
                        self.run_extra_actions(player_party_instance)
                        if current_event.post_message is not None:
                            core_io.send_output(
                                OutputMessage(current_event.post_message)
                            )
                    case "LEAVE":
                        core_io.send_output(OutputMessage("They Travel onwards"))
                    case _:
                        raise RuntimeError(
                            f"Invalid value {action} in standard_encounter "
                        )

            case EncounterType.MYSTERY:
                # this is pretty brittle right now, can be reworked later
                if current_event.pre_message is not None:
                    core_io.send_output(OutputMessage(current_event.pre_message))

                core_io.request_input(
                    UserPromptRequest(
                        prompts=["What do you do?:"],
                        options=["ATTACK", "GREET"],
                    )
                )

                match core_io.receive_input():
                    case "GREET":
                        self.execute_actor_action(targets)
                        self.run_extra_actions(player_party_instance)
                        if current_event.post_message is not None:
                            core_io.send_output(
                                OutputMessage(current_event.post_message)
                            )
                    case "ATTACK":
                        # if you attack you get attacked (this is brittle and needs work) Need to work on event triggers into other events
                        static_event: Encounter = self.find_encounter_by_id(
                            "surprise_attack"
                        )
                        static_event.execute_actor_action(targets)
                        static_event.run_extra_actions(player_party_instance)
                        if static_event.post_message is not None:
                            core_io.send_output(
                                OutputMessage(static_event.post_message)
                            )
                    case _:
                        raise ValueError("Null Action Set MonkaS")

            case EncounterType.LOOT:
                if current_event.pre_message is not None:
                    core_io.send_output(OutputMessage(current_event.pre_message))
                core_io.request_input(
                    UserPromptRequest(["What do you do?:"], ["OPEN", "LEAVE"])
                )

                match core_io.receive_input():
                    case "OPEN":
                        self.execute_actor_action(targets)
                        self.run_extra_actions(player_party_instance)
                        if current_event.post_message is not None:
                            core_io.send_output(
                                OutputMessage(current_event.post_message)
                            )
                    case "LEAVE":
                        core_io.send_output(
                            OutputMessage("You leave the chest undisturbed")
                        )
                    case _:
                        raise ValueError("Null Action Set MonkaS")

            case EncounterType.NONE:
                pass
            case _:
                raise ValueError(
                    f"Error Invalid encounter Type Call: {current_event.encounter_type}"
                )


class EffectTarget(Enum):
    ALL = "ALL"
    RANDOM = "RANDOM"


class ActorAction(Enum):
    HEAL = "HEAL"
    DAMAGE = "DAMAGE"
    GAIN_GOLD = "GAIN_GOLD"
    LOSE_GOLD = "LOSE_GOLD"
    GAIN_POTION = "GAIN_POTION"
    LOSE_POTION = "LOSE_POTION"


class EncounterEffect:
    pass


# --- #

from enum import Enum

from RPyG.actors import PlayerParty


class EffectTarget(Enum):
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


class EncounterEffect:
    kind: str
    targets: EffectTarget
    actor_action: ActorAction
    magnitude: int
    effect_messages: list[str]
    extra_effects: list[str]

    def process(self, player_party_instance: PlayerParty) -> None:
        pass


class Encounter:
    kind: str
    primary_encounter: bool
    special_encounter: bool
    prompt: str | None
    success_choice: str | None
    retry_choice: str | None
    failure_choice: str | None
    success_effects: list[EncounterEffect]
    retry_effects: list[EncounterEffect]
    failure_effects: list[EncounterEffect]
    success_messages: list[str]
    retry_messages: list[str]
    failure_messages: list[str]

    def __init__(self) -> None:
        pass

    def process(self, player_party_instance: PlayerParty) -> None:
        pass
