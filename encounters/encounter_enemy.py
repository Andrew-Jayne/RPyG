import random
import json
from actors.actor_enemy import Enemy
from combat.combat import Combat
from content.content import ENEMIES_STANDARD
from message.message import Message
from interaction.interaction import Interaction
from utilites.utilities import ensure_type


# Only for Type Checking / Hinting
from actors.actor_party import EnemyParty, PlayerParty

@staticmethod
def generate_enemy_party(enemy_party_attributes: dict ,enemy_count: int) -> EnemyParty:
    ensure_type(enemy_party_attributes, dict, 'enemy_party_attributes')
    ensure_type(enemy_count, int, 'enemy_count')

    # Create Instances & Add to Instance List
    enemy_party_instances = []
    for _ in range(0,enemy_count):
        variant_list = enemy_party_attributes['variant_lists']

        variant_grade_index = random.randint(0,(len(list(variant_list.keys())) - 1)) # set the index of the key 
        variant_grade = list(variant_list.keys())[variant_grade_index]
        
        variant_choice_index = random.randint(0,(len(enemy_party_attributes['variant_lists'][variant_grade]) - 1))
        
        enemy_party_instances.append(Enemy(enemy_party_attributes['variant_lists'][variant_grade][variant_choice_index]))

    if enemy_count is 1:
        enemy_party_name = f"Lone {enemy_party_instances[0].name}"
    else:
        enemy_party_name  = f"{enemy_party_attributes['group_name']} of {enemy_count} {enemy_party_attributes['pural_name']}"
    
    return EnemyParty(enemy_party_name, enemy_party_instances)


@staticmethod
def enemy_encounter(player_party_instance: PlayerParty) -> None:
    ensure_type(player_party_instance, PlayerParty, 'player_party_instance')
    enemy_party_attributes = {}

    enemy_chance = random.randint(0, 4)
    if enemy_chance == 6:
        raise ValueError("Random gave unexpected value for 'enemy chance'")

    # Select Enemy Type From options
    elif enemy_chance == 0 or enemy_chance == 1:
        enemy_party_attributes = random.choice(ENEMIES_STANDARD['small_enemies'])
        
    elif enemy_chance == 2 or enemy_chance == 3:
        enemy_party_attributes = random.choice(ENEMIES_STANDARD['medium_enemies'])

    elif enemy_chance == 4:
        enemy_party_attributes = random.choice(ENEMIES_STANDARD['large_enemies'])

    # Set Enemy Count
    enemy_count = int(len(player_party_instance.members) + random.randint(-2,2))
    if enemy_count <= 0:
        enemy_count = 1

    enemy_party = generate_enemy_party(enemy_party_attributes, enemy_count)


    Message.encounter_message(enemy_party.name)
    match Interaction.encounter_enemy():
        case "BATTLE":
            Combat.battle(player_party_instance, enemy_party)
        case "FLEE":
            for player_instance in player_party_instance.members:
                if player_instance.luck >= random.randint(4,15):
                    Message.flee_success_message(player_instance.name, enemy_party.name)
                else:
                    Message.flee_failure_message(player_instance.name, enemy_party.name)
                    Combat.battle(player_party_instance, enemy_party)
                    break
