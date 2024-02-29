## Automatic Interactions
import random
from logic.logic import select_combat_target


# Only Used for type Checking
from actors.actor_party import EnemyParty, PlayerParty
from actors.actor_playable import PlayableActor


def auto_enemy_encounter() -> str:
    chosen_action = random.choice(["FLEE","ATTACK"])
    return chosen_action

def auto_in_battle(player_instance:PlayableActor) -> str:
    from message.message import Message
    if not isinstance(player_instance, PlayableActor):
        raise ValueError("The 'player_instance' parameter must be of type PlayerParty. Received type: {}".format(type(player_instance).__name__))

    if player_instance.health <= 40 and player_instance.potions != 0:
        chosen_action = "HEAL" 
    elif player_instance.potions == 0:
            Message.display_message(f"{player_instance.name} has no remaining potions and must make a stand!", 1)
            chosen_action = "ATTACK"
    else:
            chosen_action = random.choice(["EVADE","ATTACK","ATTACK","ATTACK"])
    
    return chosen_action

def auto_post_battle(player_party_instance:PlayerParty) -> str:
    if not isinstance(player_party_instance, PlayerParty):
        raise ValueError("The 'player_instance' parameter must be of type PlayerParty. Received type: {}".format(type(player_party_instance).__name__))

    for player_instance in player_party_instance.members:
        if player_instance.health < 20 and player_instance.potions != 0:
            chosen_action = "HEAL"
    chosen_action = "TRAVEL"

    return chosen_action
    
def auto_choose_combat_target(enemy_party_instance:EnemyParty) -> int:
    if not isinstance(enemy_party_instance, EnemyParty):
        raise ValueError("The 'enemy_party_instance' parameter must be of type EnemyParty. Received type: {}".format(type(enemy_party_instance).__name__))

    chosen_target = select_combat_target(enemy_party_instance)

    return chosen_target


def auto_at_merchant(player_party_instance:PlayerParty) -> None:
    from message.message import Message
    if not isinstance(player_party_instance, PlayerParty):
        raise ValueError("The 'enemy_party_instance' parameter must be of type PlayerParty. Received type: {}".format(type(player_party_instance).__name__))

    #init Counts
    player_count = 0
    gold_spent = 0
    potions_sold = 0

    for player_instance in player_party_instance.members:
        player_count += 1
        while player_instance.potions < 100 and player_instance.gold != 0:
            if player_instance.spend_gold(25) == True:
                gold_spent += 25

                player_instance.gain_potion(1)
                potions_sold += 1

                Message.display_message(f"{player_instance.name} purchases a potion. They now have {player_instance.potions}", 1)
            else:
                Message.display_message(f"{player_instance.name} does not have enough Gold to purchase more potions", 1)
                break

def auto_confirm_rest() -> bool:
    return random.choice([True,True,False])

def auto_mystery_action() -> bool:
    return random.choice(["GREET","GREET","ATTACK"])

def auto_loot_action() -> bool:
    return random.choice(["OPEN","OPEN","LEAVE"])