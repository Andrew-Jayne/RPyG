import os

from RPyG.config import Config


def clear_display() -> None:
    "If the game is not in Auto Mode, will clear the display"
    config = Config.get_config()
    # Screen is not cleared in Auto mode since It's better for testing
    # Auto mode is kinda turning into a debug mode (I might make that an option at some point)
    if config.global_game_mode == "MANUAL":
        # For Windows
        if os.name == "nt":
            os.system("cls")
        # For macOS and Linux
        else:
            os.system("clear")
