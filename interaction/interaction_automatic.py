## Automatic Interactions
import random
from logic.logic import select_combat_target
from logging.logging import write_log


def auto_enemy_encounter() -> str:
    chosen_action = random.choice(["FLEE","ATTACK"])
    write_log(f"Function: auto_enemy_encounter returned value {chosen_action}")
    return chosen_action

def auto_in_battle(player_instance:object) -> str:
    if player_instance.health <= 40 and player_instance.potions != 0:
        chosen_action = "HEAL" 
    elif player_instance.potions == 0:
            print(f"{player_instance.name} has no remaining potions and must make a stand!")
            chosen_action = "ATTACK"
    else:
            chosen_action = random.choice(["EVADE","ATTACK","ATTACK","ATTACK"])
    
    write_log(f"Function: auto_in_battle returned value {chosen_action}")
    return chosen_action

def auto_post_battle(player_party_instance:object) -> str:
    for player_instance in player_party_instance.members:
        if player_instance.health < 20 and player_instance.potions != 0:
            chosen_action = "HEAL"
    chosen_action = "TRAVEL"

    write_log(f"Function: auto_post_battle returned value {chosen_action}")
    return chosen_action
    
def auto_choose_combat_target(enemy_party_instance:object) -> int:
    chosen_target = select_combat_target(enemy_party_instance)

    write_log(f"Function: auto_choose_combat_target returned value {chosen_target}")
    return chosen_target


def auto_at_merchant(player_party_instance:object) -> None:
    #Null Counts
    player_count = 0
    gold_spent = 0
    potions_sold = 0

    for player_instance in player_party_instance.members:
        player_count += 1
        while player_instance.potions < 100 and player_instance.gold != 0:
            if player_instance.gold != 0:
                player_instance.lose_gold(25)
                gold_spent += 25
                player_instance.gain_potion(1)
                potions_sold += 1
                print(f"{player_instance.name} purchases a potion. They now have {player_instance.potions}")
            else:
                print(f"{player_instance.name} does not have enough Gold to purchase more potions")
                break
    write_log(f"Function: auto_at_merchant sold {potions_sold} to {player_count} for a total of ")