import random
from encounters.encounter_enemy import enemy_encounter
from encounters.encounter_special import SpecialEncounters
from encounters.encounter_standard import standard_encounter
from message.message import Message
# Just for Type Checking
from actors.actor_party import PlayerParty

def check_for_encounter(player_party_instance:PlayerParty, empty_distance:int) -> bool:
    if not isinstance(player_party_instance, PlayerParty):
        raise ValueError("The 'player_party_instance' parameter must be of type PlayerParty. Received type: {}".format(type(player_party_instance).__name__))

    if player_party_instance.progress not in [1,25,50,75,99,100]:
        encounter_check = random.uniform(0, 1)

        if 0 <= encounter_check < 0.125:  #12.5% chance
            Message.distance_since_last(empty_distance)
            enemy_encounter(player_party_instance)
            return True
            
        elif 0.125 <= encounter_check < 0.325:  #20% chance
            Message.distance_since_last(empty_distance)
            standard_encounter(player_party_instance)
            return True
        else:
            return False
    else:              
        match player_party_instance.progress:
            case 1:
                SpecialEncounters.tavern_notice(player_party_instance)
                return True
            case 25:
                Message.distance_since_last(empty_distance)
                SpecialEncounters.friendly_keep_visit(player_party_instance)
                return True
            case 50:
                Message.distance_since_last(empty_distance)
                SpecialEncounters.midway_boss(player_party_instance)
                return True
            case 75:
                Message.distance_since_last(empty_distance)
                SpecialEncounters.enemy_keep_visit(player_party_instance)
                return True
            case 99:
                Message.distance_since_last(empty_distance)
                SpecialEncounters.penultimate_boss(player_party_instance)
                return True
            case 100:
                SpecialEncounters.final_boss(player_party_instance)
                return True
            case _:
                raise ValueError("""
                        The world goes black and You awaken in a cart, with your hands bound. 
                        
                        A man calls to you and says:
                        
                        'Hey You! Finally Awake!
                        """)
    