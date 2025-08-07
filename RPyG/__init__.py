from typing import Literal

from RPyG.content import ContentPaths
from RPyG.core_io import RPyGInterface


def launch_game(
    content_paths: ContentPaths,
    interface: RPyGInterface,
) -> None:
    from RPyG.content import ContentLibrary
    from RPyG.core_io import CoreIO
    from RPyG.encounters.encounter import check_for_encounter
    from RPyG.gameState.game_start import start_game

    # These are gateway singletons so we just need to create them
    # at a scope where they live for the lifetime of the applications
    ContentLibrary(content_paths)
    CoreIO(interface)

    player_party_instance = start_game()

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

    if player_party_instance.members != []:
        Message.post_game_recap(player_party_instance)

    # [] means all players are in the dead_members list, this is like... 5% safer than len() == 0
    # because it is looking at the list as a list rather than a property of it against an int
    else:
        Message.game_over_message(player_party_instance)


__all__ = ["RPyGInterface", "launch_game", "ContentPaths"]
