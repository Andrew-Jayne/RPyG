from argparse import ArgumentParser


DUNGEONS_STANDARD_PATH = "content/dungeons/standard"
DUNGEONS_SPECIAL_PATH = "content/dungeons/special"

ENCOUNTERS_STANDARD_PATH = "content/encounters/standard"
ENCOUNTERS_SPECIAL_PATH = "content/encounters/special"

ENEMIES_STANDARD_PATH = "content/enemies/standard"
ENEMIES_SPECIAL_PATH = "content/enemies/special"

STORY_PATH = "content/story"


def main(game_mode: str, using_default_party: bool) -> None:
    from content import ContentLibrary, ContentPaths
    from encounters.encounter import check_for_encounter
    from gameState.game_start import start_game
    from message.message import Message

    # Launch Content Library, accessed via gateway patern in consuming modules
    ContentLibrary(
        ContentPaths(
            special_dungeons_path=DUNGEONS_SPECIAL_PATH,
            standard_dungeons_path=DUNGEONS_STANDARD_PATH,
            special_encounters_path=ENCOUNTERS_SPECIAL_PATH,
            standard_encounters_path=ENCOUNTERS_SPECIAL_PATH,
            special_enemies_path=ENEMIES_SPECIAL_PATH,
            standard_enemies_path=ENEMIES_STANDARD_PATH,
            story_path=STORY_PATH,
        )
    )

    player_party_instance = start_game(game_mode, using_default_party)

    rounds_without_encounter = 0
    # The Key Loop
    while player_party_instance.progress != 100:
        player_party_instance.progress += 1
        match check_for_encounter(player_party_instance, rounds_without_encounter):
            case True:
                rounds_without_encounter = 1
            case False:
                rounds_without_encounter += 1
                Message.empty_travel_message(rounds_without_encounter)

        if len(player_party_instance.members) == 0:
            break

    if len(player_party_instance.members) == 0:
        Message.game_over_message(player_party_instance)

    else:
        Message.post_game_recap(player_party_instance)


# Main Function Wrapper to Accept and Pass Args
if __name__ == "__main__":
    parser = ArgumentParser(description="RPyG, a text based RPG in Python")
    parser.add_argument("--auto", action="store_true", help="Run in automatic mode.")
    parser.add_argument("--default", action="store_true", help="Use the Default Party")
    args = parser.parse_args()

    if args.auto is True:
        mode = "AUTO"
    else:
        mode = "MANUAL"

    if args.default is True:
        use_default_party = True
    else:
        use_default_party = False

    main(mode, use_default_party)
