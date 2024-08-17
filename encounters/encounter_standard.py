import random
from content.content import ENCOUNTERS_STANDARD
from message.message import Message
from interaction.interaction import Interaction
from utilites.utilities import ensure_type

# only used for type checking
from actors.actor_playable import PlayableActor
from actors.actor_party import PlayerParty


@staticmethod
def set_encounter_targets(current_event_targets: str, player_party_instance: PlayerParty):
    ensure_type(current_event_targets, str, 'current_event_targets')
    ensure_type(player_party_instance, PlayerParty, 'player_party_instance')

    match current_event_targets:
        case 'all':
            return player_party_instance.members
        case 'random':
            return [random.choice(player_party_instance.members)]
        case _:
            raise ValueError(f"invalid target: {current_event_targets}")
    

@staticmethod
def find_encounter_by_id(encounters_dict: dict, target_item_id: str) -> object:
    ensure_type(encounters_dict, dict, 'encounters_dict')
    ensure_type(target_item_id, str, 'target_item_id')

    # Directly access the event by its ID
    found_item = encounters_dict.get(target_item_id)
    if found_item is None:
        raise FileNotFoundError(f"Error: Unable to find an event with the ID {target_item_id}")
    return found_item



@staticmethod
def execute_actor_action(event_object: dict, target_instance_list: list[PlayableActor]) -> None:
    ensure_type(event_object, dict, 'event_object')
    ensure_type(target_instance_list, list, 'target_instance_list')

    magnitude = int(event_object['magnitude'] / len(target_instance_list))
    Message.display_message(event_object['message'], 1)

    for target in target_instance_list:
        match event_object['actor_action']:
            case "damage":
                target.damage(magnitude)
            case "heal":
                target.heal(magnitude)
            case "gain_gold":
                target.gain_gold(magnitude)
            case "lose_gold":
                target.lose_gold(magnitude)
            case "gain_potion":
                target.gain_potion(magnitude)
            case "lose_potion":
                target.lose_potion(magnitude)
            case "use_potion":
                target.use_potion()
            case _:
                raise ValueError(f"Error Invalid Method Call: {event_object['actor_action']}")


@staticmethod
def execute_special_action(event_object: dict, player_party_instance: PlayerParty):
    ensure_type(event_object, dict, 'event_object')
    ensure_type(player_party_instance, PlayerParty, 'player_party_instance')
    match event_object['special_action']:
        case "at_merchant":
            Interaction.at_merchant(player_party_instance)
        case _:
            raise ValueError(f"error invalid special_action: {event_object['special_action']}")


@staticmethod
def run_extra_actions(event_object: object, player_party_instance: PlayerParty, encounter_objects: dict) -> None:
    ensure_type(event_object, object, 'event_object')
    ensure_type(player_party_instance, PlayerParty, 'player_party_instance')
    ensure_type(encounter_objects, dict, 'encounter_objects_dict')

    # Run extra Actions if they exist
    if event_object['additional_events'] is not None:
        for event_id in event_object['additional_events']:
            new_event = find_encounter_by_id(encounter_objects, event_id)
            targets = set_encounter_targets(new_event['targets'], player_party_instance)
            execute_actor_action(new_event, targets)

     # Run Special Actions if they exist
    if event_object['special_action'] is not None:
        execute_special_action(event_object, player_party_instance)


@staticmethod
def standard_encounter(player_party_instance: PlayerParty) -> None:
    ensure_type(player_party_instance, PlayerParty, 'player_party_instance')

    current_event = ENCOUNTERS_STANDARD[random.choice(list(ENCOUNTERS_STANDARD.keys()))]

    targets = set_encounter_targets(current_event['targets'], player_party_instance)

    match current_event['encounter_type']:
        case "REST":
            Message.display_message(current_event['pre_message'], 1)
            if Interaction.confirm_rest() is True:
                execute_actor_action(current_event, targets)
                run_extra_actions(current_event, player_party_instance, ENCOUNTERS_STANDARD)
                Message.display_message(current_event['post_message'], 1)
            else:
                    Message.display_message("They Travel onwards", 1)


        case "MYSTERY":  
        # this is pretty brittle right now, can be reworked later
            Message.display_message(current_event['pre_message'], 1)
            match Interaction.mystery_action():
                case "GREET":
                    execute_actor_action(current_event, targets)
                    run_extra_actions(current_event, player_party_instance, ENCOUNTERS_STANDARD)
                    Message.display_message(current_event['post_message'], 1)
                case "ATTACK":
                    # if you attack you get attacked
                    static_event = find_encounter_by_id(ENCOUNTERS_STANDARD,'surprise_attack')
                    execute_actor_action(static_event, targets)
                    run_extra_actions(current_event, player_party_instance, ENCOUNTERS_STANDARD)
                    Message.display_message(static_event['post_message'],1)
                case _:
                        raise ValueError("Null Action Set MonkaS")


        case "LOOT":
            Message.display_message(current_event['pre_message'],1)
            match Interaction.loot_action():
                case "OPEN":
                    execute_actor_action(current_event, targets)
                    run_extra_actions(current_event, player_party_instance, ENCOUNTERS_STANDARD)
                    Message.display_message(current_event['post_message'],1)
                case "LEAVE":
                        Message.display_message("You leave the chest undisturbed",1)
                case _:
                        raise ValueError("Null Action Set MonkaS")


        case "NONE":
            pass
        case _:
            raise ValueError(f"Error Invalid encounter Type Call: {current_event['encounter_type']}")
