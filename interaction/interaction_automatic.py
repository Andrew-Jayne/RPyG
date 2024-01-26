## Automatic Interactions
import random
from logic.logic import select_combat_target
from logging.logging import write_log


def auto_enemy_encounter():
    return random.choice(["FLEE","ATTACK"])

def auto_in_battle(player_instance):
    if player_instance.health <= 4 and player_instance.potions != 0:
        return "HEAL" 
    elif player_instance.potions == 0:
            print(f"{player_instance.name} has no remaining potions and must make a stand!")
            return "ATTACK"
    else:
            return random.choice(["EVADE","ATTACK","ATTACK","ATTACK"])

def auto_post_battle(player_party_instance):
    for player_instance in player_party_instance.members:
        if player_instance.health < 20 and player_instance.potions != 0:
            return "HEAL"
    return "TRAVEL"
    
def auto_choose_combat_target(enemy_party_instance):
    return select_combat_target(enemy_party_instance)


def auto_at_merchant(player_party_instance):
    for player_instance in player_party_instance.members:
        while player_instance.potions < 100 and player_instance.gold != 0:
            if player_instance.gold != 0:
                player_instance.lose_gold(25)
                player_instance.gain_potion(1)
                print(f"{player_instance.name} purchases a potion. They now have {player_instance.potions}")
            else:
                print(f"{player_instance.name} does not have enough Gold to purchase more potions")
                break