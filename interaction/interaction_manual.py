## Manual Interactions
from interaction.interaction_utilities import validate_input

#Only Used for type checking
from actors.actor_party import PlayerParty, EnemyParty

def manual_enemy_encounter() -> str:
    encounter_options = ["BATTLE", "FLEE"]
    enounter_message = f"""
Choose an Action:
BATTLE
FLEE

"""
    return validate_input(encounter_options, enounter_message)


def manual_in_battle(player_name:str) -> str:
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
    

def manual_post_battle() -> str:
    post_battle_options = ["HEAL", "TRAVEL", "SAVE"]
    post_battle_message = """
Choose an Action:
HEAL
TRAVEL
SAVE

"""     
    return validate_input(post_battle_options, post_battle_message)

def manual_choose_combat_target(enemy_party_instance:EnemyParty) -> str:
    if not isinstance(enemy_party_instance, EnemyParty):
        raise ValueError("The 'enemy_party_instance' parameter must be of type PlayerParty. Received type: {}".format(type(enemy_party_instance).__name__))

    target_options = []
    for i in range(0,len(enemy_party_instance.members)):
        target_options.append(str(i))

    base_target_message = ["Which enemy will you attack?", ""]
    for i,member in enumerate(enemy_party_instance.members):
        base_target_message.append(f"{i} {member.name}:{member.health}")
    base_target_message.append("\n\n")

    target_message = "\n".join(base_target_message)

    return validate_input(target_options, target_message)


   
def manual_at_merchant(player_party_instance:PlayerParty) -> None:
    if not isinstance(player_party_instance, PlayerParty):
        raise ValueError("The 'player_party_instance' parameter must be of type PlayerParty. Received type: {}".format(type(player_party_instance).__name__))

    player_choice = None
    merchant_options = ["BUY", "LEAVE"]
    merchant_message = """
Choose an Action:
BUY
LEAVE
"""

    for player_instance in player_party_instance.members:
        while player_choice != "LEAVE":
            player_choice = validate_input(merchant_options, merchant_message)
            print(f"{player_instance.name} has {player_instance.potions} potions & {player_instance.gold} gold")
            if player_choice == "BUY":
                if player_instance.spend_gold(25) == True:
                    player_instance.gain_potion(1)
                    print(f"{player_instance.name} purchases a potion. They now have {player_instance.potions} & {player_instance.gold} gold")
                else:
                    print(f"{player_instance.name} does not have enough Gold to purchase more potions")
                    break