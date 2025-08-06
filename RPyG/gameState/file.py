import hashlib
import hmac
import os
import pickle

# Only used for Type Checking
from RPyG.actors import PlayerParty
from RPyG.interaction.interaction import Interaction
from RPyG.message.message import Message
from RPyG.utilites import ensure_type


# """Secret""" key for HMAC, if you break your file that's on you
secret_key = b"I_WILL_HACK_MY_SAVE_FILE_AND_PROBLEMS_WILL_BE_MY_FAULT"


def save_game(player_party_instance: PlayerParty) -> None:
    """
    Call this to Save the current state of the player party object to a pickle file then exits the program
    This serves to save all progress of the party
    """

    ensure_type(player_party_instance, PlayerParty, "player_party_instance")

    serialized_data = pickle.dumps(player_party_instance)
    signature = hmac.new(secret_key, serialized_data, hashlib.sha256).digest()

    with open("savegame.rpygs", "wb") as save_file:
        save_file.write(signature + serialized_data)
    Message.display_message(
        f"Successfully Saved Game for {player_party_instance.name}", 2
    )

    save_prompt = ["Would you like to keep playing?"]
    save_options = ["YES", "NO"]
    match Interaction.prompt_user(save_options, save_prompt):
        case "YES":
            pass
        case "NO":
            exit()
        case _:
            pass


def load_game() -> PlayerParty:
    """
    Call this to load the game stored in the pickle file called 'savegame.rpygs'.
    Any other .rpygs files will be ignored
    """
    save_file_path = "savegame.rpygs"

    # Check if the save file exists
    if not os.path.exists(save_file_path):
        raise FileNotFoundError(
            "Save file not found. Please check file path & try again, or start a new game"
        )

    with open(save_file_path, "rb") as save_file:
        content = save_file.read()
    signature, serialized_data = content[:32], content[32:]  # Assuming SHA-256 hash
    expected_signature = hmac.new(secret_key, serialized_data, hashlib.sha256).digest()

    if not hmac.compare_digest(expected_signature, signature):
        raise ValueError("Save file tampered with or corrupted.")
    player_party_instance = pickle.loads(serialized_data)

    if not isinstance(player_party_instance, PlayerParty):
        raise ValueError(
            "The 'player_party_instance' must be of type PlayerParty. Received type: {}".format(
                type(player_party_instance).__name__
            )
        )

    Message.display_message(
        f"Successfully Loaded Save Game for: {player_party_instance.name}", 1
    )
    return player_party_instance
