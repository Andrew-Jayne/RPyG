import random

from RPyG.combat import battle
from RPyG.constructs import EnemySet, StoryEvent
from RPyG.core_io import RPyGInterface
from RPyG.exceptions import ImpossibleValueException
from RPyG.utilities import ensure_type


## This funciton is pretty oversized, but this removed the entire encounter module which is pretty damn cool
def launch_game(
    content_path: str,
    interface: RPyGInterface,
) -> None:
    from RPyG.content import ContentLibrary
    from RPyG.core_io import CoreIO
    from RPyG.core_io.io_models import (
        EmptyDistanceMessage,
        OutputMessage,
        UserPromptRequest,
    )
    from RPyG.game_state.game_start import start_game

    ensure_type(content_path, str, "content_path")
    ensure_type(interface, RPyGInterface, "interface")

    # These are gateway singletons so we just need to create them
    # at a scope where they live for the lifetime of the applications
    ContentLibrary(content_path)
    ContentLibrary.validate_content()
    CoreIO(interface)

    player_party_instance = start_game()

    rounds_without_encounter = 0
    # The Key Loop
    core_io = CoreIO.get_core_io()
    content_library = ContentLibrary.get_library()
    while player_party_instance.progress != 100:
        player_party_instance.progress += 1

        library = ContentLibrary.get_library()
        if player_party_instance.progress not in library.story_events.keys():
            match random.randint(1, 8):
                case 1:  # 12.5% chance
                    core_io.send_output(
                        OutputMessage(
                            f"After {rounds_without_encounter * 10} miles of travel"
                        )
                    )
                    match random.randint(1, 5):
                        case 1 | 2:  # 40% Chance
                            enemy_set = random.choice(
                                list(content_library.small_enemies.values())
                            )
                            enemy_count = len(
                                player_party_instance.members
                            ) + random.randint(-1, 3)
                        case 3 | 4:  # 40% Chance
                            enemy_set = random.choice(
                                list(content_library.medium_enemies.values())
                            )
                            enemy_count = len(
                                player_party_instance.members
                            ) + random.randint(-2, 2)
                        case 5:  # 20% Chance
                            enemy_set = random.choice(
                                list(content_library.large_enemies.values())
                            )
                            enemy_count = len(
                                player_party_instance.members
                            ) + random.randint(-2, 1)
                        case _:
                            raise ImpossibleValueException("random.randint(1, 5)")

                    # Set Enemy Count
                    if enemy_count <= 0:
                        enemy_count = 1

                    enemy_party = EnemySet.generate_enemy_party(enemy_set, enemy_count)

                    core_io.send_output(
                        OutputMessage(f"Your Party encounters a {enemy_party.name}!")
                    )

                    core_io.request_input(
                        UserPromptRequest(
                            options=["BATTLE", "FLEE"],
                            prompts=["Choose an Action:"],
                        )
                    )
                    match core_io.receive_input():
                        case "BATTLE":
                            battle(player_party_instance, enemy_party)
                        case "FLEE":
                            for player_instance in player_party_instance.members:
                                if player_instance.luck >= random.randint(4, 15):
                                    core_io.send_output(
                                        OutputMessage(
                                            f"{player_instance.name} has Successfully Escaped the {enemy_party.name}!"
                                        )
                                    )
                                else:
                                    core_io.send_output(
                                        OutputMessage(
                                            f"{player_instance.name} has Failed to Escape the {enemy_party.name}!"
                                        )
                                    )
                                    battle(player_party_instance, enemy_party)
                                    break
                        case _:
                            raise RuntimeError()
                    rounds_without_encounter = 1
                case 2, 3:  # 25% chance
                    core_io.send_output(
                        OutputMessage(
                            f"After {rounds_without_encounter * 10} miles of travel"
                        )
                    )
                    encounter = library.get_standard_encounter()
                    encounter.run(player_party_instance)
                    rounds_without_encounter = 1
                case _:  # 62.5% chance
                    rounds_without_encounter += 1
                    core_io.send_output(
                        EmptyDistanceMessage(distance=rounds_without_encounter)
                    )
        else:
            story_event: StoryEvent = library.story_events[
                player_party_instance.progress
            ]
            story_event.trigger(player_party_instance)
            core_io.send_output(
                OutputMessage(f"After {rounds_without_encounter * 10} miles of travel")
            )
            rounds_without_encounter = 1

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
