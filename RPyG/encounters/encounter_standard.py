import math
import random

from RPyG.actors import PlayableActor, PlayerParty
from RPyG.content import ContentLibrary
from RPyG.content.encounter_library import (
    ActorAction,
    Encounter,
    EncounterTarget,
    EncounterType,
    SpecialAction,
)
from RPyG.core_io import CoreIO
from RPyG.core_io.io_models import OutputMessage, UserPromptRequest
from RPyG.utilites import ensure_type


@staticmethod
def set_encounter_targets(
    current_event_targets: EncounterTarget,
    player_party_instance: PlayerParty,
) -> list[PlayableActor]:
    ensure_type(current_event_targets, EncounterTarget, "current_event_targets")
    ensure_type(player_party_instance, PlayerParty, "player_party_instance")

    match current_event_targets:
        case EncounterTarget.ALL:
            return player_party_instance.members
        case EncounterTarget.RANDOM:
            return [random.choice(player_party_instance.members)]
        case _:
            raise ValueError(f"invalid target: {current_event_targets}")


@staticmethod
def find_encounter_by_id(
    target_item_id: str,
) -> Encounter:
    ensure_type(target_item_id, str, "target_item_id")
    content_library: ContentLibrary = ContentLibrary.get_library()

    # Directly access the event by its ID
    found_item = content_library.standard_encounters.get(target_item_id)
    if found_item is None:
        raise FileNotFoundError(
            f"Error: Unable to find an event with the ID {target_item_id}"
        )
    return found_item


@staticmethod
def execute_actor_action(
    encounter: Encounter,
    target_instance_list: list[PlayableActor],
) -> None:
    ensure_type(encounter, Encounter, "encounter")
    ensure_type(target_instance_list, list, "target_instance_list")
    for actor in target_instance_list:
        ensure_type(actor, PlayableActor, "actor")
    core_io = CoreIO.get_core_io()

    magnitude = int(encounter.magnitude / len(target_instance_list))
    if encounter.message is not None:
        core_io.send_output(OutputMessage(encounter.message))

    for target in target_instance_list:
        match encounter.actor_action:
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
                raise ValueError(f"Error Invalid Method Call: {encounter.actor_action}")


@staticmethod
def execute_special_action(encounter: Encounter, player_party_instance: PlayerParty):
    ensure_type(encounter, Encounter, "event_object")
    ensure_type(player_party_instance, PlayerParty, "player_party_instance")
    core_io = CoreIO.get_core_io()
    match encounter.special_action:
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
            raise ValueError(
                f"error invalid special_action: {encounter.special_action}"
            )


@staticmethod
def run_extra_actions(
    encounter: Encounter,
    player_party_instance: PlayerParty,
) -> None:
    ensure_type(encounter, Encounter, "encounter")
    ensure_type(player_party_instance, PlayerParty, "player_party_instance")
    # Run extra Actions if they exist
    if encounter.additional_events is not None:
        for event_id in encounter.additional_events:
            new_event: Encounter = find_encounter_by_id(event_id)
            targets = set_encounter_targets(new_event.targets, player_party_instance)
            execute_actor_action(new_event, targets)

    # Run Special Actions if they exist
    if encounter.special_action is not None:
        execute_special_action(encounter, player_party_instance)


@staticmethod
def standard_encounter(player_party_instance: PlayerParty) -> None:
    ensure_type(player_party_instance, PlayerParty, "player_party_instance")
    content_library: ContentLibrary = ContentLibrary.get_library()
    core_io = CoreIO.get_core_io()

    current_event = random.choice(list(content_library.standard_encounters.values()))

    targets = set_encounter_targets(current_event.targets, player_party_instance)

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
                    execute_actor_action(current_event, targets)
                    run_extra_actions(
                        current_event,
                        player_party_instance,
                    )
                    if current_event.post_message is not None:
                        core_io.send_output(OutputMessage(current_event.post_message))
                case "LEAVE":
                    core_io.send_output(OutputMessage("They Travel onwards"))
                case _:
                    raise RuntimeError(f"Invalid value {action} in standard_encounter ")

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
                    execute_actor_action(current_event, targets)
                    run_extra_actions(
                        current_event,
                        player_party_instance,
                    )
                    if current_event.post_message is not None:
                        core_io.send_output(OutputMessage(current_event.post_message))
                case "ATTACK":
                    # if you attack you get attacked
                    static_event: Encounter = find_encounter_by_id("surprise_attack")
                    execute_actor_action(static_event, targets)
                    run_extra_actions(
                        current_event,
                        player_party_instance,
                    )
                    core_io.send_output(OutputMessage(static_event.post_message))
                case _:
                    raise ValueError("Null Action Set MonkaS")

        case EncounterType.LOOT:
            if current_event.pre_message is not None:
                core_io.send_output(OutputMessage(current_event.pre_message))
            rest_options = ["OPEN", "LEAVE"]
            rest_message = ["What do you do?:"]
            core_io.request_input(rest_options, rest_message)

            match core_io.receive_input():
                case "OPEN":
                    execute_actor_action(current_event, targets)
                    run_extra_actions(
                        current_event,
                        player_party_instance,
                    )
                    if current_event.post_message is not None:
                        core_io.send_output(OutputMessage(current_event.post_message))
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
                f"Error Invalid encounter Type Call: {current_event['encounter_type']}"
            )
