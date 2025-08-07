from argparse import ArgumentParser
from typing import Literal

import RPyG
from interfaces import BasicTerminalInterface


DUNGEONS_STANDARD_PATH = "game_content/dungeons/standard"
DUNGEONS_SPECIAL_PATH = "game_content/dungeons/special"

ENCOUNTERS_STANDARD_PATH = "game_content/encounters/standard"
ENCOUNTERS_SPECIAL_PATH = "game_content/encounters/special"

ENEMIES_STANDARD_PATH = "game_content/enemies/standard"
ENEMIES_SPECIAL_PATH = "game_content/enemies/special"

STORY_PATH = "game_content/story"


def main(
    game_mode: Literal["AUTO", "MANUAL"],
    use_default_party: bool,
):
    RPyG.launch_game(
        content_paths=RPyG.ContentPaths(
            special_dungeons_path=DUNGEONS_SPECIAL_PATH,
            standard_dungeons_path=DUNGEONS_STANDARD_PATH,
            special_encounters_path=ENCOUNTERS_SPECIAL_PATH,
            standard_encounters_path=ENCOUNTERS_STANDARD_PATH,
            special_enemies_path=ENEMIES_SPECIAL_PATH,
            standard_enemies_path=ENEMIES_STANDARD_PATH,
            story_path=STORY_PATH,
        ),
        interface=BasicTerminalInterface(game_mode, use_default_party),
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
