import argparse

def main(mode:str,use_default:bool):
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
            if use_default == True:
                player_party_instance = PlayerParty(name="The Default Party", members=default_party())
            else:
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
            raise ValueError("Error No Valid Game Mode was selected")
    
    rounds_without_encounter = 0
    # The Key Loop
    while player_party_instance.progress != 100:
        player_party_instance.progress += 1
        if check_for_encounter(player_party_instance, rounds_without_encounter) == False:
            rounds_without_encounter += 1
            Message.empty_travel_message(rounds_without_encounter)
        else:
            rounds_without_encounter = 1

        if len(player_party_instance.members) == 0:
            break
        

    if len(player_party_instance.members) == 0:
        Message.game_over_message(player_party_instance)
        
    else:
        Message.post_game_recap(player_party_instance)


## Main Function Wrapper to Accept and Pass Args
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='RPyG, a text based RPG in Python')
    parser.add_argument('--keep-log', action='store_true', help='Keep log from previous session.')
    parser.add_argument('--auto', action='store_true', help='Run in automatic mode.')
    parser.add_argument('--default', action='store_true', help='Use the Default Party')
    args = parser.parse_args()

    mode = "AUTO" if args.auto else "MANUAL"
    use_default = True if args.default else False
    if not args.keep_log:
        pass

    
    main(mode,use_default)
