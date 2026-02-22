from contextlib import AbstractContextManager
from typing import TYPE_CHECKING, Self, final

from RPyG.actors import EnemyParty, PlayerParty
from RPyG.constructs import BorrowTrackedResource
from RPyG.utilities import ensure_type


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

    def borrow_enemy_party(self) -> AbstractContextManager[EnemyParty]:
        return self._enemy_party.borrow_resource()

    def set_enemy_party(self, enemy_party_instance: EnemyParty) -> None:
        from RPyG.actors import EnemyParty

        ensure_type(enemy_party_instance, EnemyParty, "enemy_party_instance")
        self._enemy_party.load_resource(enemy_party_instance)

    def reset_enemy_party(self) -> None:
        self._enemy_party.destroy_resource()

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
