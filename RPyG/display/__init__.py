import os

import config


def clear_display() -> None:
    "If the game is not in Auto Mode, will clear the display"
    # Screen is not cleared in Auto mode since It's better for testing
    # Auto mode is kinda turning into a debug mode (I might make that an option at some point)
    if config.GLOBAL_GAME_MODE == "MANUAL":
        # For Windows
        if os.name == "nt":
            os.system("cls")
        # For macOS and Linux
        else:
            os.system("clear")
