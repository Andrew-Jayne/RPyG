import argparse
from logging.logging import clear_log


def main(mode:str):
    import copy
    from gameState.file import load_game
    from gameState.welcome import welcome, get_start_type, party_start, default_party
    from actors.actor_playable import PlayableActor
    from actors.actor_party import PlayerParty
    from message.message import Message
    from interaction.interaction import Interaction
    from encounters.encounter import check_for_encounter
    

    welcome()

    match mode:
        case "AUTO":
            Interaction.global_game_mode = "AUTO"
            player_party_instance = PlayerParty(name="The Default Party", members=default_party())
        case "MANUAL":
            Interaction.global_game_mode = "MANUAL"
            match get_start_type():
                case "LOAD":
                    player_party_instance = load_game()
                case "NEW":
                    my_party, my_party_name = party_start()
                    my_party_instances = []
                    for member in my_party:
                        my_party_instances.append(PlayableActor(member[0], member[1]))
                    
                    player_party_instance = PlayerParty(my_party_name, my_party_instances)
        case _ :
            print("Error No Valid Game Mode was selected")
            exit()
    
    rounds_without_encounter = 0
    copy_instance = copy.deepcopy(player_party_instance)
    # The Key Loop
    while player_party_instance.progress != 101:
        if check_for_encounter(player_party_instance, rounds_without_encounter) == False:
            rounds_without_encounter += 1
            print(f"{'.' * (rounds_without_encounter - 1 )}")
        else:
            rounds_without_encounter = 1
        if len(player_party_instance.members) == 0:
            break
        player_party_instance.progress += 1


    # see the stats for all the player even if their dead (this can be improved)
    if len(player_party_instance.members) == 0:
        Message.post_game_recap(copy_instance)
        print(f"{player_party_instance.name} has failed in their quest after {player_party_instance.progress * 10} miles" , end='\n\n')
        
    else:
        Message.post_game_recap(player_party_instance)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='RPyG, a text based RPG in Python')
    parser.add_argument('--keep-log', action='store_true', help='Keep log from previous session.')
    parser.add_argument('--auto', action='store_true', help='Run in automatic mode.')
    args = parser.parse_args()

    mode = "AUTO" if args.auto else "MANUAL"

    if not args.keep_log:
        clear_log()
    
    main(mode)
