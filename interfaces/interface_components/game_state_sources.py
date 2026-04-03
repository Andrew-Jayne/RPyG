from abc import ABC, abstractmethod
from typing import Final, override

from RPyG.game_state import GameState


class GameStateHandler(ABC):
    @staticmethod
    @abstractmethod
    def load_game_state() -> GameState:
        pass

    @staticmethod
    @abstractmethod
    def save_game_state(game_state: GameState) -> None:
        pass


class PickleGameStateHandler(GameStateHandler):
    # """Secret""" key for HMAC, if you break your file that's on you
    SECRET_KEY: Final[bytes] = b"I_WILL_HACK_MY_SAVE_FILE_AND_PROBLEMS_WILL_BE_MY_FAULT"
    SAVE_FILE_PATH: Final[str] = "savegame.rpygs"

    @override
    @staticmethod
    def load_game_state() -> GameState:
        """
        Call this to load the game stored in the pickle file called 'savegame.rpygs'.
        Any other .rpygs files will be ignored
        """
        import hashlib
        import hmac
        import os
        import pickle

        from RPyG.core_io import CoreIO, output_models
        from RPyG.exceptions import ImpossibleValueException
        from RPyG.utilities import ensure_type

        core_io = CoreIO.get_core_io()

        # Check if the save file exists
        if os.path.exists(PickleGameStateHandler.SAVE_FILE_PATH) is False:
            raise FileNotFoundError(
                "Save file not found. Please check file path & try again, or start a new game"
            )

        with open(PickleGameStateHandler.SAVE_FILE_PATH, "rb") as save_file:
            content = save_file.read()
        signature, serialized_data = content[:32], content[32:]  # Assuming SHA-256 hash
        expected_signature = hmac.new(
            PickleGameStateHandler.SECRET_KEY,
            serialized_data,
            hashlib.sha256,
        ).digest()

        match hmac.compare_digest(expected_signature, signature):
            case True:
                game_state: GameState = pickle.loads(serialized_data)
            case False:
                raise RuntimeError("Save file tampered with or corrupted.")
            case _:  # pyright: ignore[reportUnnecessaryComparison]
                raise ImpossibleValueException(  # pyright: ignore[reportUnreachable]
                    "Save File tampering is so bad that compare_digest did not return a bool MonkaS"
                )

        ensure_type(game_state, GameState, "game_state")

        core_io.send_output(
            output_models.OutputMessage(
                f"Successfully Loaded Save Game for: {game_state.player_party.name}"
            )
        )
        ## yuck but I am moving off of pickle soon anyways
        GameState._instance = game_state  # pyright: ignore[reportPrivateUsage]
        return game_state

    @override
    @staticmethod
    def save_game_state(game_state: GameState) -> None:
        """
        Call this to Save the current state of the player party object to a pickle file then exits the program
        This serves to save all progress of the party
        """
        import hashlib
        import hmac
        import pickle
        import sys

        from RPyG.core_io import CoreIO, input_models, output_models
        from RPyG.utilities import ensure_type

        ensure_type(game_state, GameState, "game_state")

        serialized_data = pickle.dumps(game_state)
        signature = hmac.new(
            PickleGameStateHandler.SECRET_KEY,
            serialized_data,
            hashlib.sha256,
        ).digest()

        with open("savegame.rpygs", "wb") as save_file:
            save_file.write(signature + serialized_data)  # pyright: ignore[reportUnusedCallResult]

        core_io = CoreIO.get_core_io()
        core_io.send_output(
            output_models.OutputMessage(
                f"Successfully Saved Game for {game_state.player_party.name}"
            )
        )

        core_io.request_str_input(
            input_models.UserPromptRequest(
                options=["YES", "NO"],
                prompts=["Would you like to keep playing?"],
            )
        )
        match core_io.receive_str_input():
            case "YES":
                core_io.send_output(
                    output_models.OutputMessage("The adventure continues!")
                )
            case "NO":
                sys.exit(0)
            case _:
                raise ValueError("Must be a choice of 'YES' or 'NO'")
