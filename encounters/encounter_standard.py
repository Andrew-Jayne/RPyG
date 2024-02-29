import json
import random
from message.message import Message
from interaction.interaction import Interaction

#only used for type checking
from actors.actor_playable import PlayableActor
from actors.actor_party import PlayerParty



# Update Encounter Declaration to be a key of ID with a value of Encounter data, current model will not scale well with large encounter lists
def find_encounter_by_id(full_item_list:list, target_item_id:str) -> object:
        found_item = None
        for active_item in full_item_list:
              if active_item['id'] == target_item_id:
                   found_item = active_item
                   return found_item
        if found_item == None:
             raise FileNotFoundError(f"Error Unable to Find an Event with the ID {target_item_id}")


def execute_actor_action(event_object:object, target_instance_list:list[PlayableActor]) -> None:
    magnitude = int(event_object['magnitude'] / len(target_instance_list))
    actor_method_name = event_object['actor_action'].lower()
    Message.display_message(event_object['message'], 1)
    
    for target in target_instance_list:
        actor_method_to_call = getattr(target, actor_method_name)
        if callable(actor_method_to_call) == True:
            actor_method_to_call(magnitude)
        else:
            raise ValueError(f"Error Invalid Method Call: {actor_method_name}, {actor_method_to_call}")


def execute_special_action(event_object:object, target_instance_list:list[PlayableActor]) -> None:
            # Run Actions for Encounter
            special_method_name = event_object['special_action'].lower()
            special_method_call = getattr(Interaction, special_method_name)
            if callable(special_method_call) == True:
                special_method_call(target_instance_list)
            else:
                raise ValueError(f"error invalid special_action: {event_object['special_action']}")

def run_extra_actions(event_object:object, player_party_instance:PlayerParty,encounters_objects_list:list) -> None:
    allowed_special_actions = ["at_merchant",]
    # Run extra Actions if they exist
    if event_object['additional_events'] != None:
        for event_id in event_object['additional_events']:
            new_event = find_encounter_by_id(encounters_objects_list['events'],event_id)
            match new_event['targets']:
                case 'all':
                    targets = player_party_instance.members
                case 'random':
                    targets = [random.choice(player_party_instance.members)]
                case _:
                    raise ValueError(f"invalid target: {event_object['targets']}")
            execute_actor_action(new_event, targets)
    
    # Validate Special action
    if event_object['special_action'] != None:
        if event_object['special_action'] in allowed_special_actions:
            execute_special_action(event_object,player_party_instance)
        else:
            raise ValueError(f"error invalid special_action: {event_object['special_action']}")

def standard_encounter(player_party_instance:PlayerParty) -> None:

    allowed_actor_actions = [  "damage","heal","gain_gold","lose_gold","gain_potion","lose_potion","use_potion"]
    

    with open('encounters/standard_encounters.json', 'r') as encounters_file:
        encounters_objects_list = json.load(encounters_file)
        current_event = random.choice(encounters_objects_list['events'])

    match current_event['targets']:
        case 'all':
            targets = player_party_instance.members
        case 'random':
            targets = [random.choice(player_party_instance.members)]
        case _:
            raise ValueError(f"invalid target: {current_event['targets']}")

    if current_event['actor_action'] in allowed_actor_actions:
        match current_event['encounter_type']:
            case "REST":
                    Message.display_message(current_event['pre_message'], 1)
                    if Interaction.confirm_rest() == True:
                        execute_actor_action(current_event, targets)
                        run_extra_actions(current_event,player_party_instance,encounters_objects_list)
                        Message.display_message(current_event['post_message'], 1)
                    else:
                         Message.display_message("They Travel onwards", 1)
            case "MYSTERY": ## this is pretty brittle right now, can be reworked later 
                    Message.display_message(current_event['pre_message'], 1)
                    match Interaction.mystery_action():
                        case "GREET":
                            execute_actor_action(current_event, targets)
                            run_extra_actions(current_event,player_party_instance,encounters_objects_list)
                            Message.display_message(current_event['post_message'], 1)
                        case "ATTACK":
                            static_event = find_encounter_by_id(encounters_objects_list['events'],'surprise_attack')
                            execute_actor_action(static_event,targets) ## if you attack you get attacked
                            run_extra_actions(current_event,player_party_instance,encounters_objects_list)
                            Message.display_message(static_event['post_message'],1)
                        case _:
                              raise ValueError("Null Action Set MonkaS")
            case "LOOT":
                    Message.display_message(current_event['pre_message'],1)
                    match Interaction.loot_action():
                        case "OPEN":
                            execute_actor_action(current_event, targets)
                            run_extra_actions(current_event,player_party_instance,encounters_objects_list)
                            Message.display_message(current_event['post_message'],1)
                        case "LEAVE":
                              Message.display_message("You leave the chest undisturbed",1)
                        case _:
                              raise ValueError("Null Action Set MonkaS")
            case "NONE":
                  pass
            case _:
                    raise ValueError(f"Error Invalid encounter Type Call: {current_event['encounter_type']}")
    else:
        raise ValueError(f"Error Invalid Method Call: {current_event['actor_action']}")
        







    match current_event['actor_action']:
        case "damage":
              pass
        case "heal":
              pass
        case "gain_gold":
              pass
        case "lose_gold":
              pass
        case "gain_potion":
              pass
        case "lose_potion":
              pass
        case "use_potion":
              pass
        case _:
              raise ValueError(f"Error Invalid Method Call: {current_event['actor_action']}")