## Manual Interactions
from interaction.interaction_utilities import validate_input

def manual_enemy_encounter():
    encounter_options = ["BATTLE", "FLEE"]
    enounter_message = f"""
Choose an Action:
BATTLE
FLEE

"""
    return validate_input(encounter_options, enounter_message)


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
    return validate_input(post_battle_options, post_battle_message)


def manual_choose_combat_target(enemy_party_instance):
    target_options = []
    for i in range(0,len(enemy_party_instance.members)):
        target_options.append(str(i))

    base_target_message = ["Which enemy will you attack?", ""]
    for i,member in enemy_party_instance.members:
        base_target_message.append(f"{i} {member.name}:{member.health}")

    target_message = "\n".join(base_target_message)

    return validate_input(target_options, target_message)
    