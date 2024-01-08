def main():
    import pickle
    from actors.actor_playable import PlayableActor
    from actors.actor_party import PlayerParty
    from message.message import Message
    from interaction.interaction import Interaction
    from encounters.encounter import check_for_encounter
    from welcome import welcome, get_start_type, party_start, default_party

    welcome()
    if Interaction.global_game_mode == "MANUAL":
        match get_start_type():
            case "LOAD":
                with open('savegame.rpygs', 'rb') as file:
                    # Write some text to the file.
                    player_party_instance = pickle.load(file) # (maybe some way to make that safer or add a checksum or hash)
                    print(f"Successfully Loaded Save Game for: {player_party_instance.name}")
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
    main()