import random
import json
from actors.actor_enemy import Enemy
from actors.actor_party import EnemyParty
from combat.combat import Combat
from message.message import Message
from interaction.interaction import Interaction

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
enemy_count = int(3 + random.randint(-2,2))
if enemy_count == 0:
    enemy_count = 1

# Create Instances & Add to Instance List
enemy_party_instances = []
enemy_count = 1
for _ in range(0,enemy_count):
    variant_list = enemy_party_attributes['variant_lists']
    variant_list_length = len(list(variant_list.keys())) # get total number of variants
    variant_grade_index = random.randint(0,(variant_list_length - 1)) # set the index of the key 
    variant_grade = list(variant_list.keys())[variant_grade_index]
    variant_index_max = len(enemy_party_attributes['variant_lists'][variant_grade]) - 1
    variant_choice_index = random.randint(0,variant_index_max)
    variant_dict = enemy_party_attributes['variant_lists'][variant_grade][variant_choice_index]
    enemy_instance = Enemy(variant_dict)


   # enemy_party_instances.append()

#default_enemy_instance = Enemy(enemy_instance)



