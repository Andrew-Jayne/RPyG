import random
from enum import Enum

from RPyG.actors import EnemyParty, PlayerParty
from RPyG.core_io import CoreIO
from RPyG.core_io.io_models import (
    EmptyDistanceMessage,
    OutputMessage,
    UserPromptRequest,
)
from RPyG.exceptions import ImpossibleValueException
from RPyG.game_state.startup import get_player_party_instance
from RPyG.utilities import ensure_type, setup_logger


logger = setup_logger(__name__)


class EncounterType(Enum):
    EnemyEncounter = "EnemyEncounter"
    StandardEncounter = "StandardEncounter"


def generate_enemy_set(player_count: int):
    from RPyG.constructs import EnemySet
    from RPyG.content import ContentLibrary

    ensure_type(player_count, int, "player_count")

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

    ensure_type(player_party_instance, PlayerParty, "player_party_instance")
    ensure_type(enemy_party_instance, EnemyParty, "enemy_party_instance")

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


def check_for_encounter() -> EncounterType | None:
    match random.randint(1, 8):
        case 1:  # 12.5% chance
            return EncounterType.EnemyEncounter
        case 2 | 3:  # 25% chance
            return EncounterType.StandardEncounter
        case _:  # 62.5% chance
            return None


def play_game():
    from RPyG.constructs import StoryEvent
    from RPyG.content import ContentLibrary

    core_io = CoreIO.get_core_io()
    content_library = ContentLibrary.get_library()
    player_party_instance = get_player_party_instance()

    # Check if player is in a dungeon
    logger.info("Checking if player is in a dungeon")
    if player_party_instance.in_dungeon is True:
        if player_party_instance.active_dungeon is not None:
            logger.info("Player is in dungeon, resuming")
            player_party_instance.active_dungeon.traverse_dungeon(player_party_instance)
    else:
        logger.info("Player is not in dungeon")

    rounds_without_encounter = 1
    while player_party_instance.progress != 100:
        player_party_instance.progress += 1
        if player_party_instance.progress in content_library.story_events.keys():
            core_io.send_output(
                OutputMessage(f"After {rounds_without_encounter * 10} miles of travel")
            )
            story_event: StoryEvent = content_library.story_events[
                player_party_instance.progress
            ]
            story_event.trigger(player_party_instance)
        else:
            check_result = check_for_encounter()
            if check_result is not None:
                core_io.send_output(
                    OutputMessage(
                        f"After {rounds_without_encounter * 10} miles of travel"
                    )
                )
                match check_result:
                    case EncounterType.EnemyEncounter:
                        handle_enemy_encounter(
                            player_party_instance=player_party_instance,
                            enemy_party_instance=generate_enemy_set(
                                len(player_party_instance.members)
                            ),
                        )
                    case EncounterType.StandardEncounter:
                        encounter = content_library.get_standard_encounter()
                        encounter.process_encounter(player_party_instance)
                rounds_without_encounter = 1
            else:
                rounds_without_encounter += 1
                core_io.send_output(
                    EmptyDistanceMessage(distance=rounds_without_encounter)
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
