from RPyG.content import ContentPaths
from RPyG.core_io import RPyGInterface
from RPyG.utilites import ensure_type


def launch_game(
    content_paths: ContentPaths,
    interface: RPyGInterface,
) -> None:
    from RPyG.content import ContentLibrary
    from RPyG.core_io import CoreIO
    from RPyG.core_io.io_models import EmptyDistanceMessage, OutputMessage
    from RPyG.encounters.encounter import check_for_encounter
    from RPyG.gameState.game_start import start_game

    ensure_type(content_paths, ContentPaths, "content_paths")
    ensure_type(interface, RPyGInterface, "interface")

    # These are gateway singletons so we just need to create them
    # at a scope where they live for the lifetime of the applications
    ContentLibrary(content_paths)
    CoreIO(interface)

    player_party_instance = start_game()

    rounds_without_encounter = 0
    # The Key Loop
    core_io = CoreIO.get_core_io()
    while player_party_instance.progress != 100:
        player_party_instance.progress += 1
        match check_for_encounter(player_party_instance, rounds_without_encounter):
            case True:
                rounds_without_encounter = 1
            case False:
                rounds_without_encounter += 1
                core_io.send_output(EmptyDistanceMessage(rounds_without_encounter))

        if len(player_party_instance.members) == 0:
            break

    if player_party_instance.members == []:
        # [] means all players are in the dead_members list, this is like... 5% safer than len() == 0
        # because it is looking at the list as a list rather than a property of it against an int
        core_io.send_output(
            OutputMessage(
                f"{player_party_instance.name} has failed in their quest after {player_party_instance.progress * 10} miles"
            )
        )

    core_io.send_output(OutputMessage(player_party_instance.end_game_report()))
