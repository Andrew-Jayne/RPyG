import pickle

def save_game(player_party_instance:object) -> None:
    """
    Call this to Save the current state of the player party object to a pickle file. 
    This serves to save all progress of the party
    """
    with open('savegame.rpygs', 'wb') as save_file:
                pickle.dump(player_party_instance, save_file)
                print(f"Successfully Saved Game for: {player_party_instance.name}")
                exit()

def load_game() -> object:
    """
    Call this to load the pickle stored in the file called 'savegame.rpygs'.
    Any other .rpygs files will be ignored, the loaded file is not checked so hack with care as you may break your game :MonkaS
    """

    with open('savegame.rpygs', 'rb') as save_file:
        player_party_instance = pickle.load(save_file) # (maybe some way to make that safer or add a checksum or hash)
        print(f"Successfully Loaded Save Game for: {player_party_instance.name}")

        ## TODO Add Saftey Checks
    return player_party_instance