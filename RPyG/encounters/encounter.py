import random

# Just for Type Checking
from RPyG.actors import PlayerParty
from RPyG.content import ContentLibrary
from RPyG.core_io import CoreIO
from RPyG.core_io.io_models import OutputMessage
from RPyG.encounters.encounter_enemy import enemy_encounter
from RPyG.encounters.encounter_special import SpecialEncounters
from RPyG.encounters.encounter_standard import standard_encounter
from RPyG.utilites import ensure_type


## TODO, this needs some work, but the whole story system is due for updates so it's fine for now


def send_distance_traveled_message(empty_distance: int):
    core_io = CoreIO.get_core_io()
    core_io.send_output(OutputMessage(f"After {empty_distance * 10} miles of travel"))


def check_for_encounter(
    player_party_instance: PlayerParty,
    empty_distance: int,
) -> bool:
    ensure_type(player_party_instance, PlayerParty, "player_party_instance")
    library = ContentLibrary.get_library()

    if player_party_instance.progress not in library.story_events.keys():
        encounter_check = random.uniform(
            0, 1
        )  # I don't like how this is done, and I find it awkward to read

        if 0 <= encounter_check < 0.125:  # 12.5% chance
            send_distance_traveled_message(empty_distance)
            enemy_encounter(player_party_instance)
            return True

        elif 0.125 <= encounter_check < 0.325:  # 20% chance
            send_distance_traveled_message(empty_distance)
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
                send_distance_traveled_message(empty_distance)
                SpecialEncounters.friendly_keep_visit(player_party_instance)
                return True
            case 50:
                send_distance_traveled_message(empty_distance)
                SpecialEncounters.midway_boss(player_party_instance)
                return True
            case 75:
                send_distance_traveled_message(empty_distance)
                SpecialEncounters.enemy_keep_visit(player_party_instance)
                return True
            case 99:
                send_distance_traveled_message(empty_distance)
                SpecialEncounters.penultimate_boss(player_party_instance)
                return True
            case 100:
                SpecialEncounters.final_boss(player_party_instance)
                return True
            case _:
                raise RuntimeError(
                    """
                        The world goes black and You awaken in a cart, with your hands bound. 
                        
                        A man calls to you and says:
                        
                        'Hey You! Finally Awake!'
                        """
                )
