## Automatic Interactions
import random

def auto_enemy_encounter():
    encounter_action = random.choice(["FLEE","ATTACK"])
    return encounter_action

def auto_in_battle(player_instance):
    if player_instance.health <= 4 and player_instance.potions != 0:
        return "HEAL" 
    elif player_instance.potions == 0:
            print("You have no remaining potions and must make a stand!")
            return "ATTACK"
    else:
            return "ATTACK"

def auto_post_battle(player_instance):
    if player_instance.health < 20 and player_instance.potions != 0:
        return "HEAL"
    else:
             return "TRAVEL"