## Automatic Interactions
import random

def auto_enemy_encounter():
    return random.choice(["FLEE","ATTACK"])

def auto_in_battle(player_instance):
    if player_instance.health <= 4 and player_instance.potions != 0:
        return "HEAL" 
    elif player_instance.potions == 0:
            print("You have no remaining potions and must make a stand!")
            return "ATTACK"
    else:
            return random.choice(["EVADE","ATTACK","ATTACK","ATTACK"])

def auto_post_battle(player_instance):
    if player_instance.health < 20 and player_instance.potions != 0:
        return "HEAL"
    else:
        return "TRAVEL"