import argparse
from logging.logging import clear_log

def main():
    from gameState.file import load_game
    from actors.actor_playable import PlayableActor
    from actors.actor_party import PlayerParty
    from message.message import Message
    from interaction.interaction import Interaction
    from encounters.encounter import check_for_encounter
    from gameState.welcome import welcome, get_start_type, party_start, default_party

    welcome()
    if Interaction.global_game_mode == "MANUAL":
        match get_start_type():
            case "LOAD":
                player_party_instance = load_game()
            case "NEW":
                my_party, my_party_name = party_start()
                my_party_instances = []
                for member in my_party:
                    my_party_instances.append(PlayableActor(member[0], member[1]))
                
                player_party_instance = PlayerParty(my_party_name, my_party_instances)
    else:
        player_party_instance = PlayerParty(name="The Default Party", members=default_party())

    # The Key Loop
    while player_party_instance.progress < 100:
        player_party_instance.progress += 1
        Message.party_progress_message(player_party_instance)
        check_for_encounter(player_party_instance)
        if len(player_party_instance.members) == 0:
            print(f"{player_party_instance.name} has failed in their quest after {player_party_instance.progress * 10} miles" , end='\n\n')
            break

    Message.post_game_recap(player_party_instance)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='RPyG, a text based RPG in Python')
    parser.add_argument('--keep-log', action='store_true', help='Keep log from previous session.')
    #parser.add_argument('--automatic', action='auto_true', help='this does not work right now :)') # Waiting for full implementaion
    args = parser.parse_args()
    if args.keep_log != True:
        clear_log()
    main()