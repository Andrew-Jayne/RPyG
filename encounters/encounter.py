import random
from encounters.encounter_enemy import enemy_encounter
from encounters.encounter_special import SpecialEncounters
from encounters.encounter_standard import standard_encounter

def check_for_encounter(player_party_instance) -> None:

    if player_party_instance.progress not in [25,50,75,99,100]:
        encounter_check = random.uniform(0, 1)

        if 0 <= encounter_check < 0.125:  #12.5% chace
            enemy_encounter(player_party_instance)
            
        elif 0.125 <= encounter_check < 0.325:  #20% chance
            standard_encounter(player_party_instance)
    else:              
        match player_party_instance.progress:
            case 25:
                SpecialEncounters.friendly_keep_visit(player_party_instance)
            case 50:
                SpecialEncounters.midway_boss(player_party_instance)
            case 75:
                SpecialEncounters.enemy_keep_visit(player_party_instance)
            case 99:
                SpecialEncounters.penultimate_boss(player_party_instance)
            case 100:
                SpecialEncounters.final_boss(player_party_instance)
            case _:
                print("""
                        The world goes black and You awaken in a cart, with your hands bound. 
                        
                        A man calls to you and says:
                        
                        'Hey You! Finally Awake!
                        """)