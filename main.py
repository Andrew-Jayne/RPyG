from argparse import ArgumentParser
from typing import Literal

import RPyG
from interfaces import BasicTerminalInterface


CONTENT_PATH = "game_content"


def main(
    game_mode: Literal["AUTO", "MANUAL"],
    use_default_party: bool,
):
    RPyG.launch_game(
        content_path=CONTENT_PATH,
        interface=BasicTerminalInterface(
            game_mode,
            use_default_party,
        ),
    )


# Main Function Wrapper to Accept and Pass Args
if __name__ == "__main__":
    parser = ArgumentParser(description="RPyG, a text based RPG in Python")
    parser.add_argument("--auto", action="store_true", help="Run in automatic mode.")
    parser.add_argument("--default", action="store_true", help="Use the Default Party")
    args = parser.parse_args()

    if args.auto is True:
        game_mode = "AUTO"
    else:
        game_mode = "MANUAL"

    if args.default is True:
        use_default_party = True
    else:
        use_default_party = False

    main(game_mode, use_default_party)
