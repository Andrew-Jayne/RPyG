import random
import json
from actors.actor_enemy import Enemy
from actors.actor_party import EnemyParty
from combat.combat import Combat
from message.message import Message
from interaction.interaction import Interaction


def enemy_encounter(player_party):
    enemy_chance = random.randint(0,4)
    with open('encounters/enemies_common.json', 'r') as enemies_file:
        enemies_lists = json.load(enemies_file)
    if enemy_chance == 6:
        print("WTF, You're not supposed to see this, some kind of Cosmic bit flip happened")

    # Select Enemy Type From options
    elif enemy_chance == 0 or enemy_chance == 1:
        enemy_party_attributes = random.choice(enemies_lists['small_enemies'])
        
    elif enemy_chance == 2 or enemy_chance == 3:
        enemy_party_attributes = random.choice(enemies_lists['medium_enemies'])

    elif enemy_chance == 4:
        enemy_party_attributes = random.choice(enemies_lists['large_enemies'])

    #Set Enemy Count
    enemy_count = int(len(player_party.members) + random.randint(-2,2))
    if enemy_count == 0:
        enemy_count = 1

    # Create Instances & Add to Instance List
    enemy_party_instances = []
    for _ in range(0,enemy_count):
        variant_list = enemy_party_attributes['variant_lists']

        variant_grade_index = random.randint(0,(len(list(variant_list.keys())) - 1)) # set the index of the key 
        variant_grade = list(variant_list.keys())[variant_grade_index]
        
        variant_choice_index = random.randint(0,(len(enemy_party_attributes['variant_lists'][variant_grade]) - 1))
        
        enemy_party_instances.append(Enemy(enemy_party_attributes['variant_lists'][variant_grade][variant_choice_index]))
    
        
    if enemy_count == 1:
        enemy_party_name = f"Lone {enemy_party_instances[0].name}"
    else:
        enemy_party_name  = f"{enemy_party_attributes['group_name']} of {enemy_count} {enemy_party_attributes['pural_name']}"
    
    enemy_party = EnemyParty(enemy_party_name, enemy_party_instances)


    
    Message.encounter_message(enemy_party_name)
    player_action = Interaction.encounter_enemy()
    match player_action:
        case "BATTLE":
                Combat.battle(player_party, enemy_party)
        case "FLEE":
            for player_instance in player_party.members:
                if player_instance.luck >= random.randint(4,15):
                    Message.flee_success_message(player_instance.name, enemy_party_name)
                else:
                    Message.flee_failure_message(player_instance.name, enemy_party_name)
                    Combat.battle(player_party, enemy_party)
                    break  
                


## Add party name to enemies, pack of X, group of Y, lone Z


