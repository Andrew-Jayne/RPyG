import json
import random
from gameState.welcome import default_party
from actors.actor_party import PlayerParty

player_party_instance = PlayerParty(name="The Default Party", members=default_party())

def select_dungeon(target_item_id:str) -> object:
    if target_item_id == 'GENERIC': #select random when no ID is set
        with open('encounters/standard_dungeons.json', 'r') as dungeon_file:
            dungeon_list = json.load(dungeon_file)
            selected_dungeon = random.choice(dungeon_list['dungeons'])

    else: # Select from specials with ID when Set
        with open('encounters/special_dungeons.json', 'r') as dungeon_file:
            dungeon_list = json.load(dungeon_file)
            all_dungeons = dungeon_list['dungeons']
            found_item = None
            for active_item in all_dungeons:
                if active_item['id'] == target_item_id:
                    selected_dungeon = active_item
            if found_item == None:
                raise FileNotFoundError(f"Error Unable to Find an Event with the ID {target_item_id}")

    return selected_dungeon


def dungeon_encounter(player_party_instance:PlayerParty, dungeon_id:str) -> None:
    if not isinstance(player_party_instance, PlayerParty):
        raise ValueError("The 'player_party_instance' parameter must be of type PlayerParty. Received type: {}".format(type(player_party_instance).__name__))
    active_dungeon = select_dungeon(dungeon_id)

    print(active_dungeon)
    dungeon_length = active_dungeon['length']
    dungeon_name = active_dungeon ['name']
    dungeon_enemies = active_dungeon['enemies']
    dungeon_boss = active_dungeon['boss']
    print(f"""
d_len is {str(dungeon_length)}
d_name is {dungeon_name}
d_enem is {dungeon_enemies}
d_boss is {dungeon_boss}
          """)
    


dungeon_encounter(player_party_instance, 'algolons_fortess')