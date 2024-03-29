## Manual Interactions
from interaction.interaction_utilities import validate_input

#Only Used for type checking
from actors.actor_party import PlayerParty, EnemyParty
from actors.actor_playable import PlayableActor

def manual_enemy_encounter() -> str:
    encounter_options = ["BATTLE", "FLEE"]
    encounter_message = f"""
Choose an Action:
BATTLE
FLEE

"""
    return validate_input(encounter_options, encounter_message)


def manual_in_battle(player_instance:PlayableActor) -> str:
    from message.message import Message
    battle_options = ["ATTACK", f"{player_instance.special_attack_name}", f"{player_instance.react_action}", "HEAL"]
    battle_message = f"""
{player_instance.name}
Choose an Action:
ATTACK
{player_instance.special_attack_name}
{player_instance.react_action}
HEAL

"""
    battle_choice = validate_input(battle_options, battle_message)
    dumb_check = 0
    while battle_choice == "HEAL" and player_instance.is_fully_healed() == True:
        dumb_check += 1
        Message.display_message(f"{player_instance.name} is fully healed, it would be unwise to use a potion", 1)
        battle_choice = validate_input(battle_options, battle_message)
        if dumb_check > 10:
            Message.display_message("Stubborn aren't you, fine waste the damn potion", 1)
            battle_choice = "HEAL"
            break
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
    import math
    from message.message import Message

    if not isinstance(player_party_instance, PlayerParty):
        raise ValueError("The 'player_party_instance' parameter must be of type PlayerParty. Received type: {}".format(type(player_party_instance).__name__))

    player_choice = None
    merchant_options = ["BUY", "LEAVE", "BUY MAX"]

    for player_instance in player_party_instance.members:
        merchant_message = f"""
{player_instance.name}
Gold: {player_instance.gold}
Potions: {player_instance.potions}

Choose an Action:
BUY
LEAVE
BUY MAX
"""
        
        while player_choice != "LEAVE":
            player_choice = validate_input(merchant_options, merchant_message)
            Message.display_message(f"{player_instance.name} has {player_instance.potions} potions & {player_instance.gold} gold", 1)
            match player_choice:
                case "BUY":
                    if player_instance.spend_gold(25) == True:
                        player_instance.gain_potion(1)
                        Message.display_message(f"{player_instance.name} purchases a potion. They now have {player_instance.potions} & {player_instance.gold} gold", 1)
                    else:
                        Message.display_message(f"{player_instance.name} does not have enough Gold to purchase more potions", 1)
                        player_choice = "LEAVE"
                case "BUY MAX":
                    ## Using floor to make sure you can't buy 10 potions with 245 gold
                    rounds = math.floor(player_instance.gold / 25)
                    player_instance.spend_gold((round * 25))
                    player_instance.gain_potion(rounds)
                    player_choice = "LEAVE"
                case "LEAVE":
                    player_choice = "LEAVE"


def manual_confirm_rest() -> bool:
    player_choice = None
    rest_options = ["YES", "NO"]
    rest_message = """
Will you Rest here?:
YES
NO

"""
    player_choice = validate_input(rest_options, rest_message)

    match player_choice:
        case "YES":
            return True
        case "NO":
            return False
        case _:
            return True
        
def manual_mystery_action() -> str:
    player_choice = None
    rest_options = ["ATTACK", "GREET"]
    rest_message = """
What do you do?:
ATTACK
GREET

"""
    player_choice = validate_input(rest_options, rest_message)

    return player_choice
    
        

def manual_loot_action() -> bool:
    player_choice = None
    rest_options = ["OPEN", "LEAVE"]
    rest_message = """
What do you do?:
OPEN
LEAVE

"""
    player_choice = validate_input(rest_options, rest_message)

    return player_choice

        
def manual_embark() -> bool: ## i can make this funnier
    from message.message import Message
    player_choice = None
    rest_options = ["EMBARK", "DRINK"]
    rest_message = """
What shall the party do?

EMBARK
DRINK

"""
    
    player_choice = validate_input(rest_options, rest_message)

    match player_choice:
        case "EMBARK":
            return True
        case "DRINK":
            Message.display_message("After many drinks, the kings missive sticks in your mind.", 1)
            if manual_embark() == True:
                return True
        case _:
            return True
        

def manual_accept_quest() -> bool:
    from message.message import Message
    player_choice = None
    rest_options = ["ACCEPT", "DECLINE"]
    rest_message = """
Will you accept this quest from the King?

ACCEPT
DECLINE

"""
    
    player_choice = validate_input(rest_options, rest_message)

    match player_choice:
        case "ACCEPT":
            return True
        case "DECLINE":
            Message.display_message("The King insists, and asks again", 1)
            if manual_accept_quest() == True:
                return True
        case _:
            return True