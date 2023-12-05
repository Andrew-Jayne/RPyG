import random
import json
import copy
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

    elif enemy_chance == 0 or enemy_chance == 1:
        enemy_attributes = random.choice(enemies_lists['small_enemies'])
        
    elif enemy_chance == 2 or enemy_chance == 3:
        enemy_attributes = random.choice(enemies_lists['medium_enemies'])

    elif enemy_chance == 4:
        enemy_attributes = random.choice(enemies_lists['large_enemies'])

    default_enemy_instance = Enemy(
        name=enemy_attributes['name'],
        health=enemy_attributes['health'],
        strength=enemy_attributes['strength'],
        intellect=enemy_attributes['intellect'],
        agility=enemy_attributes['agility'],
        luck=enemy_attributes['luck'],
        attack_name=enemy_attributes['attack_name'])
    
    enemy_count = int(len(player_party.members) + random.randint(-2,2))
    if enemy_count == 0:
        enemy_count = 1

    enemy_party_instances = []
    for _ in range(0,enemy_count):
        enemy_party_instances.append(copy.deepcopy(default_enemy_instance))
    
    enemy_party = EnemyParty(enemy_party_instances)


    
    Message.encounter_message(default_enemy_instance.name)
    player_action = Interaction.encounter_enemy()
    match player_action:
        case "BATTLE":
                Combat.battle(player_party, enemy_party)
        case "FLEE":
            for player_instance in player_party.members:
                if player_instance.luck >= random.randint(4,15):
                    Message.flee_success_message(player_instance.name, default_enemy_instance.name)
                else:
                    Message.flee_failure_message(player_instance.name, default_enemy_instance.name)
                    Combat.battle(player_party, enemy_party)
                    break  
                


## Add party name to enemies, pack of X, group of Y, lone Z


