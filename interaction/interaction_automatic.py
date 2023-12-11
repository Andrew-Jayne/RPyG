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

def auto_post_battle(player_party_instance):
    for player_instance in player_party_instance.members:
        if player_instance.health < 20 and player_instance.potions != 0:
            return "HEAL"
    return "TRAVEL"
    
def auto_choose_combat_target(enemy_party_instance):
    enemy_max_index = len(enemy_party_instance.members) - 1
    if enemy_max_index >= 0:
        enemy_max_index = 0 ## Hack, debugging stuff will fix later 
    try: 
        return str(random.randint(0,enemy_max_index))
    except:
         import pdb; pdb.set_trace()
    #plan, 3 options: Random, Highest Atk power, lowest health (choose 1 at random on each turn, plan to use this for enemies as well)

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