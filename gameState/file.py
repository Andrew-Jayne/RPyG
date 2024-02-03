import pickle
import hmac
import hashlib
import os

# Only used for Type Checking
from actors.actor_party import PlayerParty

# """Secret""" key for HMAC, if you break your file that's on you
secret_key = b"I_WILL_HACK_MY_SAVE_FILE_AND_PROBLEMS_WILL_BE_MY_FAULT"

def save_game(player_party_instance: PlayerParty) -> None:
    """
    Call this to Save the current state of the player party object to a pickle file then exits the program 
    This serves to save all progress of the party
    """

    if not isinstance(player_party_instance, PlayerParty):
        raise ValueError("The 'player_party_instance' parameter must be of type PlayerParty. Received type: {}".format(type(player_party_instance).__name__))

    serialized_data = pickle.dumps(player_party_instance)
    signature = hmac.new(secret_key, serialized_data, hashlib.sha256).digest()

    with open('savegame.rpygs', 'wb') as save_file:
        save_file.write(signature + serialized_data)
    print(f"Successfully Saved Game for: {player_party_instance.name}")
    exit()

def load_game() -> PlayerParty:
    """
    Call this to load the game stored in the pickle file called 'savegame.rpygs'.
    Any other .rpygs files will be ignored
    """
    save_file_path = 'savegame.rpygs'
    
    # Check if the save file exists
    if not os.path.exists(save_file_path):
        raise FileNotFoundError("Save file not found. Please check the file path and try again.")
    

    with open(save_file_path, 'rb') as save_file:
        content = save_file.read()
    signature, serialized_data = content[:32], content[32:]  # Assuming SHA-256 hash
    expected_signature = hmac.new(secret_key, serialized_data, hashlib.sha256).digest()

    if not hmac.compare_digest(expected_signature, signature):
        raise ValueError("Save file tampered with or corrupted.")
    player_party_instance = pickle.loads(serialized_data)

    if not isinstance(player_party_instance, PlayerParty):
        raise ValueError("The 'player_party_instance' must be of type PlayerParty. Received type: {}".format(type(player_party_instance).__name__))

    print(f"Successfully Loaded Save Game for: {player_party_instance.name}")
    return player_party_instance