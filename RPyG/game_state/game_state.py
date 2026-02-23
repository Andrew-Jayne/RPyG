from contextlib import AbstractContextManager
from typing import TYPE_CHECKING, Self, final

from RPyG.constructs import BorrowTrackedResource, EnemyParty, PlayerParty

## blegh, these things need to go elsewhere
from RPyG.game_state.state_functions import (
    EncounterType,
    check_for_encounter,
    handle_enemy_encounter,
)
from RPyG.utilities import ensure_type, setup_logger


logger = setup_logger(__name__)

if TYPE_CHECKING is True:
    from RPyG.constructs import Dungeon


@final
class GameState:
    player_party: PlayerParty
    progress: int
    _dungeon_progress: int | None
    _enemy_party: BorrowTrackedResource[EnemyParty]
    _dungeon: BorrowTrackedResource[Dungeon]
    _instance: Self | None = None
    __slots__: tuple[str, ...] = (
        "player_party",
        "_enemy_party",
        "_dungeon",
        "progress",
        "_dungeon_progress",
    )

    def __init__(self, player_party: PlayerParty):
        from RPyG.constructs import Dungeon

        ensure_type(player_party, PlayerParty, "player_party")
        if GameState._instance is None:
            GameState._instance = self
            self.player_party = player_party
            self.progress = 0
            self._dungeon_progress = None
            self._enemy_party = BorrowTrackedResource(EnemyParty)
            self._dungeon = BorrowTrackedResource(Dungeon)
        else:
            raise RuntimeError("GameState already initialized")

    @classmethod
    def get_game_state(cls) -> "GameState":
        if GameState._instance is not None:
            return GameState._instance
        else:
            raise RuntimeError(
                "Attempted to access GameState instance before initialization"
            )

    def validate(self) -> None:
        # Ensure type and validate on all object, to runtime check at load
        valid = True
        if valid is not True:
            raise RuntimeError(" GameState failed to validate")
        return

    # core loop of the whole game
    def play_game(self):
        from RPyG.constructs import StoryEvent
        from RPyG.content import ContentLibrary
        from RPyG.core_io import CoreIO, output_models
        from RPyG.game_state import GameState

        core_io = CoreIO.get_core_io()
        game_state = GameState.get_game_state()
        content_library = ContentLibrary.get_library()

        # Check if player is in a dungeon
        logger.info("Checking if player is in a dungeon")
        if self.dungeon_progress is not None:
            logger.info("Player is in dungeon, resuming")
            with self.borrow_dungeon() as dungeon:
                dungeon.traverse_dungeon()
        else:
            logger.info("Player is not in dungeon")

        rounds_without_encounter = 1
        while self.progress != 100:
            self.progress += 1
            if str(self.progress) in content_library.story_events.keys():
                core_io.send_output(
                    output_models.OutputMessage(
                        f"After {rounds_without_encounter * 10} miles of travel"
                    )
                )
                story_event: StoryEvent = content_library.story_events[
                    str(self.progress)
                ]
                story_event.trigger()
            else:
                check_result = check_for_encounter()
                if check_result is not None:
                    core_io.send_output(
                        output_models.OutputMessage(
                            f"After {rounds_without_encounter * 10} miles of travel"
                        )
                    )
                    match check_result:
                        case EncounterType.EnemyEncounter:
                            handle_enemy_encounter()
                        case EncounterType.StandardEncounter:
                            encounter = content_library.get_standard_encounter()
                            encounter.process_encounter()
                        case EncounterType.DungeonEncoutner:
                            game_state.set_dungeon(
                                content_library.get_standard_dungeon()
                            )
                            with game_state.borrow_dungeon() as dungeon:
                                dungeon.traverse_dungeon()
                    rounds_without_encounter = 1
                else:
                    rounds_without_encounter += 1
                    core_io.send_output(
                        output_models.EmptyDistanceMessage(
                            distance=rounds_without_encounter
                        )
                    )

            if self.player_party.members == []:
                break

        if self.player_party.members == []:
            # [] means all players are in the dead_members list, this is like... 5% safer than len() == 0
            # because it is looking at the list as a list rather than a property of it against an int
            core_io.send_output(
                output_models.OutputMessage(
                    f"{self.player_party.name} has failed in their quest after {self.progress * 10} miles"
                )
            )

        core_io.send_output(
            output_models.OutputMessage(self.player_party.end_game_report())
        )

    ## Borrow Checked Dungeon Handling

    def borrow_dungeon(self) -> AbstractContextManager[Dungeon]:
        return self._dungeon.borrow_resource()

    @property
    def dungeon_progress(self) -> int | None:
        return self._dungeon_progress

    def set_dungeon(self, dungeon_instance: Dungeon) -> None:
        from RPyG.constructs import Dungeon

        ensure_type(dungeon_instance, Dungeon, "dungeon_instance")
        self._dungeon.load_resource(dungeon_instance)
        # progress can only be set to a non None value by this function
        # Helps avoid racy behavoir
        self._dungeon_progress = 0

    def progress_dungeon(self, progress_amount: int) -> None:
        # have to check the _ version to make the type checker happy
        if self._dungeon_progress is None:
            raise RuntimeError()
        # can't be zero, and can't be more than len of the dungeon
        with self.borrow_dungeon() as dungeon:
            if dungeon.length < progress_amount or progress_amount < 0:
                raise ValueError()

        self._dungeon_progress += progress_amount

    def reset_dungeon(self) -> None:
        self._dungeon.destroy_resource()
        self._dungeon_progress = None

    ## Borrow Checked Enemy Party Handling

    def borrow_enemy_party(self) -> AbstractContextManager[EnemyParty]:
        return self._enemy_party.borrow_resource()

    def set_enemy_party(self, enemy_party_instance: EnemyParty) -> None:
        ensure_type(enemy_party_instance, EnemyParty, "enemy_party_instance")
        self._enemy_party.load_resource(enemy_party_instance)

    def reset_enemy_party(self) -> None:
        self._enemy_party.destroy_resource()
