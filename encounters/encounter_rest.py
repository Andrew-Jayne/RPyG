import random
import json
from interaction.interaction import Interaction

def rest_encounter(party_instance):
    rest_chance = random.randint(0,3)
    with open('encounters/rest_common.json', 'r') as encounters_file:
        encounters_lists = json.load(encounters_file)
    if rest_chance in range(0,2):
        encounter_grade = 'minor_rest'
    elif rest_chance == 2:
        encounter_grade = 'medium_rest'
    elif rest_chance == 3:
        encounter_grade = 'large_rest'

    encounter_sub_choice = random.randint(0, len(encounters_lists[encounter_grade]) - 1)
    print(f"{encounters_lists[encounter_grade][encounter_sub_choice]['message']}", end="\n\n")
    for member_instance in party_instance.members:
        member_instance.heal(encounters_lists['minor_rest'][encounter_sub_choice]['recovery_amount'])

    if encounter_grade == 'large_rest':
        for member_instance in party_instance.members:
            Interaction.at_merchant(member_instance)