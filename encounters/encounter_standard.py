import json
import random
from interaction.interaction import Interaction

def find_encounter_by_id(full_item_list:list, target_item_id:str):
        found_item = None
        for active_item in full_item_list:
              if active_item['id'] == target_item_id:
                   found_item = active_item
                   return found_item
        if found_item == None:
             print(f"Error Unable to Find an Event with the ID {target_item_id}")
             exit()

def execute_actor_action(event_object:object, target_instance_list:list):
    print(event_object['message'])
    for target in target_instance_list:
        magnitude = int(event_object['magnitude'] / len(target_instance_list))
        actor_method_name = event_object['actor_action']
        actor_method_to_call = getattr(target, actor_method_name, None)
        if callable(actor_method_to_call) == True:
            actor_method_to_call(magnitude)
        else:
            print(f"Error Invalid Method Call: {actor_method_name}")
            exit()

def execute_special_action(event_object:object, target_instance_list:list):
            # Run Actions for Encounter
            special_method_name = event_object['special_action']
            special_method_call = getattr(Interaction, special_method_name, None)
            if callable(special_method_call) == True:
                special_method_call(target_instance_list)
            else:
                print(f"error invalid special_action: {event_object['special_action']}")

def standard_encounter(player_party_instance):

    allowed_actor_actions = [  "damage","heal","gain_gold","lose_gold","gain_potion","lose_potion","use_potion"]
    allowed_special_actions = ["at_merchant",]

    with open('encounters/standard_encounters.json', 'r') as encounters_file:
        encounters_objects_list = json.load(encounters_file)
        current_event = random.choice(encounters_objects_list['events'])

    #Setup target for encounter action


    # validate actor_action
    if current_event['actor_action'] in allowed_actor_actions:
        match current_event['targets']:
            case 'all':
                targets = player_party_instance.members
            case 'random':
                targets = [random.choice(player_party_instance.members)]
            case _:
                print(f"invalid target: {current_event['targets']}")
                exit()
        execute_actor_action(current_event, targets)
    else:
        print(f"Error Invalid Method Call: {current_event['actor_action']}")

    # Run extra Actions if they exist
    if current_event['additional_events'] != None:
        for event_id in current_event['additional_events']:
            new_event = find_encounter_by_id(encounters_objects_list['events'],event_id)
            match new_event['targets']:
                case 'all':
                    targets = player_party_instance.members
                case 'random':
                    targets = [random.choice(player_party_instance.members)]
                case _:
                    print(f"invalid target: {current_event['targets']}")
                    exit()
            execute_actor_action(new_event, targets)
    
    # Validate Special action
    if current_event['special_action'] != None:
        if current_event['special_action'] in allowed_special_actions:
            execute_special_action(current_event,player_party_instance)
        else:
            print(f"error invalid special_action: {current_event['special_action']}")
