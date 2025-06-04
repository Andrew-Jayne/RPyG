import os

import config


class Display:
    @staticmethod
    def clear_display() -> None:
        "If the game is not in Auto Mode, will clear the display"
        # Screen is not cleared in Auto mode since It's better for testing
        # Auto mode is kinda turning into a debug mode (I might make that an option at some point)
        print("called clear_display()")
        print(config.GLOBAL_GAME_MODE)
        print(os.name)
        if config.GLOBAL_GAME_MODE == "MANUAL":
            print("manual mode is enabled")
            print(f"os.name is {os.name}")
            # For Windows
            if os.name == "nt":
                os.system("cls")
            # For macOS and Linux
            else:
                print("the screen will now clear (in theory)")
                os.system("clear")
