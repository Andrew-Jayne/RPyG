import hashlib
import hmac
import os
import pickle

# Only used for Type Checking
from RPyG.actors import PlayerParty
from RPyG.core_io import CoreIO
from RPyG.core_io.io_models import OutputMessage, UserPromptRequest
from RPyG.utilities import ensure_type


# """Secret""" key for HMAC, if you break your file that's on you
secret_key = b"I_WILL_HACK_MY_SAVE_FILE_AND_PROBLEMS_WILL_BE_MY_FAULT"


def save_game(player_party_instance: PlayerParty) -> None:
    """
    Call this to Save the current state of the player party object to a pickle file then exits the program
    This serves to save all progress of the party
    """

    ensure_type(player_party_instance, PlayerParty, "player_party_instance")
    core_io = CoreIO.get_core_io()

    serialized_data = pickle.dumps(player_party_instance)
    signature = hmac.new(secret_key, serialized_data, hashlib.sha256).digest()

    with open("savegame.rpygs", "wb") as save_file:
        save_file.write(signature + serialized_data)

    core_io.send_output(
        OutputMessage(f"Successfully Saved Game for {player_party_instance.name}")
    )

    core_io.request_input(
        UserPromptRequest(
            options=["YES", "NO"],
            prompts=["Would you like to keep playing?"],
        )
    )
    match core_io.receive_input():
        case "YES":
            core_io.send_output(OutputMessage("The adventure continues"))
        case "NO":
            core_io.send_output(OutputMessage("exit process requested"))
        case _:
            raise ValueError("Must be a choice of 'YES' or 'NO'")


def load_game() -> PlayerParty:
    """
    Call this to load the game stored in the pickle file called 'savegame.rpygs'.
    Any other .rpygs files will be ignored
    """
    save_file_path = "savegame.rpygs"
    core_io = CoreIO.get_core_io()

    # Check if the save file exists
    if not os.path.exists(save_file_path):
        raise FileNotFoundError(
            "Save file not found. Please check file path & try again, or start a new game"
        )

    with open(save_file_path, "rb") as save_file:
        content = save_file.read()
    signature, serialized_data = content[:32], content[32:]  # Assuming SHA-256 hash
    expected_signature = hmac.new(secret_key, serialized_data, hashlib.sha256).digest()

    match hmac.compare_digest(expected_signature, signature):
        case True:
            player_party_instance: PlayerParty = pickle.loads(serialized_data)
        case False:
            raise ValueError("Save file tampered with or corrupted.")
        case _:
            raise RuntimeError(
                "Save File tampering is so bad that compare_digest did not return a bool MonkaS"
            )

    ensure_type(player_party_instance, PlayerParty, "player_party_instance")

    core_io.send_output(
        OutputMessage(
            f"Successfully Loaded Save Game for: {player_party_instance.name}"
        )
    )
    return player_party_instance
