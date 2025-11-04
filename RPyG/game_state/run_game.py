import random

from RPyG.actors import EnemyParty, PlayableActor, PlayerParty
from RPyG.core_io import CoreIO
from RPyG.core_io.io_models import (
    EmptyDistanceMessage,
    OutputMessage,
    UserPromptRequest,
)
from RPyG.exceptions import ImpossibleValueException
from RPyG.game_state.file import load_game
from RPyG.game_state.startup import default_party, get_start_type, party_start
from RPyG.utilities import ensure_type


def generate_enemy_set(player_count: int):
    from RPyG.constructs import EnemySet
    from RPyG.content import ContentLibrary

    content_library = ContentLibrary.get_library()
    match random.randint(1, 5):
        case 1 | 2:  # 40% Chance
            enemy_set = random.choice(list(content_library.small_enemies.values()))
            enemy_count = player_count + random.randint(-1, 3)
        case 3 | 4:  # 40% Chance
            enemy_set = random.choice(list(content_library.medium_enemies.values()))
            enemy_count = player_count + random.randint(-2, 2)
        case 5:  # 20% Chance
            enemy_set = random.choice(list(content_library.large_enemies.values()))
            enemy_count = player_count + random.randint(-2, 1)
        case _:
            raise ImpossibleValueException("random.randint(1, 5)")

    if enemy_count <= 0:
        enemy_count = 1

    return EnemySet.generate_enemy_party(enemy_set, enemy_count)


def handle_enemy_encounter(
    player_party_instance: PlayerParty,
    enemy_party_instance: EnemyParty,
):
    from RPyG.combat import battle

    core_io = CoreIO.get_core_io()
    core_io.send_output(
        OutputMessage(f"Your Party encounters a {enemy_party_instance.name}!")
    )

    core_io.request_input(
        UserPromptRequest(
            options=["BATTLE", "FLEE"],
            prompts=["Choose an Action:"],
        )
    )
    match core_io.receive_input():
        case "BATTLE":
            battle(player_party_instance, enemy_party_instance)
        case "FLEE":
            for player_instance in player_party_instance.members:
                if player_instance.luck >= random.randint(4, 15):
                    core_io.send_output(
                        OutputMessage(
                            f"{player_instance.name} has Successfully Escaped the {enemy_party_instance.name}!"
                        )
                    )
                else:
                    core_io.send_output(
                        OutputMessage(
                            f"{player_instance.name} has Failed to Escape the {enemy_party_instance.name}!"
                        )
                    )
                    battle(player_party_instance, enemy_party_instance)
                    break
        case _:
            raise RuntimeError()


def check_for_encounter(
    player_party_instance: PlayerParty,
    rounds_without_encounter: int,
) -> bool:
    from RPyG.content import ContentLibrary

    core_io = CoreIO.get_core_io()
    content_library = ContentLibrary.get_library()
    match random.randint(1, 8):
        case 1:  # 12.5% chance
            core_io.send_output(
                OutputMessage(f"After {rounds_without_encounter * 10} miles of travel")
            )

            handle_enemy_encounter(
                player_party_instance=player_party_instance,
                enemy_party_instance=generate_enemy_set(
                    len(player_party_instance.members)
                ),
            )

            return True
        case 2, 3:  # 25% chance
            core_io.send_output(
                OutputMessage(f"After {rounds_without_encounter * 10} miles of travel")
            )
            encounter = content_library.get_standard_encounter()
            encounter.process_encounter(player_party_instance)

            return True

        case _:  # 62.5% chance
            core_io.send_output(EmptyDistanceMessage(distance=rounds_without_encounter))
            return False


def run_story_event(
    player_party_instance: PlayerParty,
    rounds_without_encounter: int,
):
    from RPyG.constructs import StoryEvent
    from RPyG.content import ContentLibrary

    core_io = CoreIO.get_core_io()
    content_library = ContentLibrary.get_library()
    story_event: StoryEvent = content_library.story_events[
        player_party_instance.progress
    ]
    story_event.trigger(player_party_instance)
    core_io.send_output(
        OutputMessage(f"After {rounds_without_encounter * 10} miles of travel")
    )


def play_game():
    from RPyG.content import ContentLibrary

    core_io = CoreIO.get_core_io()
    content_library = ContentLibrary.get_library()

    # Get Player Party Instance from file or create a new one
    match get_start_type():
        case "LOAD":
            player_party_instance = load_game()
        case "NEW":
            my_party, my_party_name = party_start()
            my_party_instances: list[PlayableActor] = []
            for member in my_party:
                my_party_instances.append(PlayableActor(member[0], member[1]))
            player_party_instance = PlayerParty(my_party_name, my_party_instances)
        case "USE_DEFAULT":
            player_party_instance = default_party()
        case _:
            raise ValueError("Invalid Game Start Type")

    # Check if player is in a dungeon
    if player_party_instance.in_dungeon is True:
        if player_party_instance.active_dungeon is not None:
            player_party_instance.active_dungeon.traverse_dungeon(player_party_instance)

    rounds_without_encounter = 1
    while player_party_instance.progress != 100:
        player_party_instance.progress += 1
        if player_party_instance.progress not in content_library.story_events.keys():
            if (
                check_for_encounter(
                    player_party_instance,
                    rounds_without_encounter,
                )
                is True
            ):
                rounds_without_encounter = 1
            else:
                rounds_without_encounter += 1
        else:
            run_story_event(
                player_party_instance,
                rounds_without_encounter,
            )

        if player_party_instance.members == []:
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
