## Manual Interactions
from interaction.interaction_utilities import validate_input

def manual_enemy_encounter():
    encounter_options = ["BATTLE", "FLEE"]
    enounter_message = f"""
Choose an Action:
BATTLE
FLEE

"""
    encounter_choice = validate_input(encounter_options, enounter_message)
    return encounter_choice


def manual_in_battle(player_name):
    battle_options = ["ATTACK", "EVADE", "HEAL"]
    battle_message = f"""
{player_name}
Choose an Action:
ATTACK
EVADE
HEAL

"""
    battle_choice = validate_input(battle_options, battle_message)
    return battle_choice
    

def manual_post_battle():
    post_battle_options = ["HEAL", "TRAVEL", "SAVE"]
    post_battle_message = """
Choose an Action:
HEAL
TRAVEL
SAVE

"""     
    post_battle_choice = validate_input(post_battle_options, post_battle_message)
    return post_battle_choice
