import random
from enum import Enum
from typing import TYPE_CHECKING

from RPyG.utilities import ensure_type


if TYPE_CHECKING is True:
    from RPyG.constructs import EnemyParty


## why the TF is this here?
class EncounterType(Enum):
    EnemyEncounter = "EnemyEncounter"
    StandardEncounter = "StandardEncounter"
    DungeonEncounter = "DungeonEncounter"


def generate_enemy_set(player_count: int) -> EnemyParty:
    from RPyG.constructs import EnemySet, RandomResultItem, RandomResultTable
    from RPyG.content import ContentLibrary

    ensure_type(player_count, int, "player_count")
    content_library = ContentLibrary.get_library()

    # wholly Type hint batman!
    enemy_configs: list[RandomResultItem[tuple[list[EnemySet], int, int]]] = [
        RandomResultItem(
            (list(content_library.small_enemies.values()), -1, 3),
            0.4,
        ),
        RandomResultItem(
            (list(content_library.medium_enemies.values()), -1, 3),
            0.4,
        ),
        RandomResultItem(
            (list(content_library.large_enemies.values()), -2, 1),
            0.2,
        ),
    ]

    enemy_table = RandomResultTable(enemy_configs)

    enemy_list, offset_min, offset_max = enemy_table.generate_result()

    enemy_count = player_count + random.randint(offset_min, offset_max)
    if enemy_count <= 0:
        enemy_count = 1

    enemy_set = random.choice(enemy_list)

    return EnemySet.generate_enemy_party(enemy_set, enemy_count)


def check_for_encounter() -> EncounterType | None:
    from RPyG.constructs import RandomResultItem, RandomResultTable

    return RandomResultTable[EncounterType | None](
        [
            RandomResultItem(EncounterType.EnemyEncounter, (1 / 8)),
            RandomResultItem(EncounterType.StandardEncounter, (1 / 4)),
            RandomResultItem(EncounterType.DungeonEncounter, (1 / 10)),
            RandomResultItem(None, (5 / 8)),
        ]
    ).generate_result()


def handle_enemy_encounter():
    from RPyG.combat import battle
    from RPyG.core_io import CoreIO, input_models, output_models
    from RPyG.game_state import GameState

    game_state = GameState.get_game_state()
    core_io = CoreIO.get_core_io()
    game_state.set_enemy_party(generate_enemy_set(len(game_state.player_party.members)))
    with game_state.borrow_enemy_party() as enemy_party:
        core_io.send_output(
            output_models.EnemyEncounterMessage(enemy_party_name=enemy_party.name)
        )

        core_io.request_str_input(
            input_models.UserPromptRequest(
                options=["BATTLE", "FLEE"],
                prompts=["Choose an Action:"],
            )
        )
        flee_success = False
        match core_io.receive_str_input():
            case "BATTLE":
                pass
            case "FLEE":
                for player_instance in game_state.player_party.members:
                    flee_success = True
                    if player_instance.luck <= random.randint(4, 15):
                        flee_success = False
                    core_io.send_output(
                        output_models.FleeResultMessage(
                            success=flee_success,
                            actor_name=player_instance.name,
                            enemy_party_name=enemy_party.name,
                        )
                    )
                    if flee_success is False:
                        break
            case _:
                raise RuntimeError()

    # this is way out here so the borrow on enemy party is
    # released before the battle starts, so the enemy party
    # can be disposed of by the battle function itself
    if flee_success is False:
        battle()
