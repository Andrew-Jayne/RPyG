import json
import random
from interaction.interaction import Interaction

def standard_encounter(player_party_instance):
    allowed_actor_actions = [  "damage","heal","gain_gold","lose_gold","gain_potion","lose_potion","use_potion"]
    allowed_special_actions = ["at_merchant",]

    with open('encounters/standard_encounters.json', 'r') as encounters_file:
        encounters_objects_list = json.load(encounters_file)
        active_encounter = random.choice(encounters_objects_list['events'])

    #Setup target for encounter action
    match active_encounter['targets']:
        case 'all':
            targets = player_party_instance.members
        case 'random':
            targets = [random.choice(player_party_instance.members)]
        case _:
            print(f"invalid target: {active_encounter['targets']}")
            exit()

    # validate actor_action
    if active_encounter['actor_action'] in allowed_actor_actions:
        # Run Actions for Encounter
        print(active_encounter['message'])

        for target in targets:
            magnitude = int(active_encounter['magnitude'] / len(targets))
            actor_method_name = active_encounter['actor_action']
            actor_method_to_call = getattr(target, actor_method_name, None)
            if callable(actor_method_to_call) == True:
                actor_method_to_call(magnitude)
            else:
                print(f"Error Invalid Method Call: {actor_method_name}")
                exit()
    else:
        print(f"Error Invalid Method Call: {active_encounter['actor_action']}")
    
    # Validate Speccial action
    if active_encounter['special_action'] != None:
        if active_encounter['special_action'] in allowed_special_actions:
            # Run Actions for Encounter
            special_method_name = active_encounter['special_action']
            special_method_call = getattr(Interaction, special_method_name, None)
            if callable(actor_method_to_call) == True:
                special_method_call(player_party_instance)
            else:
                print(f"error invalid special_action: {active_encounter['special_action']}")
        else:
            print(f"error invalid special_action: {active_encounter['special_action']}")
