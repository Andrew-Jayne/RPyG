import random
from encounters.encounter_rest import rest_encounter
from encounters.encounter_enemy import enemy_encounter
from encounters.encounter_special import SpecialEncounters
from encounters.encounter_mystery import mystery_encounter

def check_for_encounter(player_instance):

    if player_instance.progress not in [25,50,75,99,100]:
        encounter_check = random.uniform(0, 1)

        if 0 <= encounter_check < 0.125:  # First 12.5% range
            enemy_encounter(player_instance)
            
        elif 0.125 <= encounter_check < 0.25:  # Second 12.5% range
            rest_encounter(player_instance)
            
        elif 0.25 <= encounter_check < 0.30:  # 5% Chance
            mystery_encounter(player_instance)
    else:              
        match player_instance.progress:
            case 25:
                SpecialEncounters.friendly_keep_visit(player_instance)
            case 50:
                SpecialEncounters.midway_boss(player_instance)
            case 75:
                SpecialEncounters.enemy_keep_visit(player_instance)
            case 99:
                SpecialEncounters.penultimate_boss(player_instance)
            case 100:
                SpecialEncounters.final_boss(player_instance)
            case _:
                print("""
                        The world goes black and You awaken in a cart, with your hands bound. 
                        
                        A man calls to you and says:
                        
                        'Hey You! Finally Awake!
                        """)