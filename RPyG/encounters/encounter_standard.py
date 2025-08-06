import random

from actors import PlayableActor, PlayerParty
from content import ContentLibrary
from content.encounter_library import (
    ActorAction,
    Encounter,
    EncounterLibrary,
    EncounterTarget,
    EncounterType,
    SpecialAction,
)
from interaction.interaction import Interaction
from message.message import Message
from utilites import ensure_type


@staticmethod
def set_encounter_targets(
    current_event_targets: EncounterTarget, player_party_instance: PlayerParty
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
    from content import ContentLibrary

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

    magnitude = int(encounter.magnitude / len(target_instance_list))
    if encounter.message is not None:
        Message.display_message(encounter.message, 1)

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
    match encounter.special_action:
        case SpecialAction.AT_MERCHANT:
            Interaction.at_merchant(player_party_instance)
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

    current_event = random.choice(list(content_library.standard_encounters.values()))

    targets = set_encounter_targets(current_event.targets, player_party_instance)

    match current_event.encounter_type:
        case EncounterType.REST:
            if current_event.pre_message is not None:
                Message.display_message(current_event.pre_message, 1)
            if Interaction.confirm_rest() is True:
                execute_actor_action(current_event, targets)
                run_extra_actions(
                    current_event,
                    player_party_instance,
                )
                if current_event.post_message is not None:
                    Message.display_message(current_event.post_message, 1)
            else:
                Message.display_message("They Travel onwards", 1)

        case EncounterType.MYSTERY:
            # this is pretty brittle right now, can be reworked later
            if current_event.pre_message is not None:
                Message.display_message(current_event.pre_message, 1)
            match Interaction.mystery_action():
                case "GREET":
                    execute_actor_action(current_event, targets)
                    run_extra_actions(
                        current_event,
                        player_party_instance,
                    )
                    if current_event.post_message is not None:
                        Message.display_message(current_event.post_message, 1)
                case "ATTACK":
                    # if you attack you get attacked
                    static_event: Encounter = find_encounter_by_id("surprise_attack")
                    execute_actor_action(static_event, targets)
                    run_extra_actions(
                        current_event,
                        player_party_instance,
                    )
                    Message.display_message(static_event.post_message, 1)
                case _:
                    raise ValueError("Null Action Set MonkaS")

        case EncounterType.LOOT:
            if current_event.pre_message is not None:
                Message.display_message(current_event.pre_message, 1)
            match Interaction.loot_action():
                case "OPEN":
                    execute_actor_action(current_event, targets)
                    run_extra_actions(
                        current_event,
                        player_party_instance,
                    )
                    if current_event.post_message is not None:
                        Message.display_message(current_event.post_message, 1)
                case "LEAVE":
                    Message.display_message("You leave the chest undisturbed", 1)
                case _:
                    raise ValueError("Null Action Set MonkaS")

        case EncounterType.NONE:
            pass
        case _:
            raise ValueError(
                f"Error Invalid encounter Type Call: {current_event['encounter_type']}"
            )
