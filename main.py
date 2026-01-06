from argparse import ArgumentParser
from typing import Literal

import RPyG
from interfaces import BasicTerminalInterface


CONTENT_PATH = "game_content"


def main(
    game_mode: Literal["AUTO", "MANUAL"],
):
    RPyG.launch_game(
        content_path=CONTENT_PATH,
        interface=BasicTerminalInterface(
            game_mode,
        ),
    )


# Main Function Wrapper to Accept and Pass Args
if __name__ == "__main__":
    parser = ArgumentParser(description="RPyG, a text based RPG in Python")
    parser.add_argument(  # pyright: ignore[reportUnusedCallResult]
        "--auto",
        action="store_true",
        help="Run in automatic mode.",
    )
    args = parser.parse_args()

    # argparse just be like that
    if args.auto is True:
        game_mode = "AUTO"
    else:
        game_mode = "MANUAL"

    main(game_mode)
