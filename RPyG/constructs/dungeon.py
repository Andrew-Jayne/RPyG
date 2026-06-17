import random
from enum import StrEnum
from typing import TYPE_CHECKING

from RPyG.utilities import ensure_type


if TYPE_CHECKING is True:
    from RPyG.constructs import EnemyActor, EnemySet


class DungeonEvent(StrEnum):
    HEAL_ROOM = "HEAL_ROOM"
    SHORTCUT = "SHORTCUT"
    BATTLE_ENEMY = "BATTLE_ENEMY"
    NOTHING = "NOTHING"


class Dungeon:
    dungeon_name: str
    start_message: str
    shortcut_message: str
    heal_room_message: str
    boss_encounter_message: str
    boss_enemy_id: str
    enemy_set_id: str
    length: int
    special_dungeon: bool
    __slots__: tuple[str, ...] = (
        "dungeon_name",
        "start_message",
        "shortcut_message",
        "heal_room_message",
        "boss_encounter_message",
        "boss_enemy_id",
        "enemy_set_id",
        "length",
        "special_dungeon",
    )

    def __init__(
        self,
        kind: str,
        name: str,
        length: int,
        special_dungeon: bool,
        boss_enemy_id: str,
        enemy_set_id: str,
        start_message: str,
        shortcut_message: str,
        heal_room_message: str,
        boss_encounter_message: str,
    ):
        ensure_type(kind, str, "kind")
        ensure_type(name, str, "name")
        ensure_type(length, int, "length")
        ensure_type(special_dungeon, bool, "special_dungeon")
        ensure_type(boss_enemy_id, str, "boss_enemy_id")
        ensure_type(enemy_set_id, str, "enemy_set_id")
        ensure_type(start_message, str, "start_message")
        ensure_type(shortcut_message, str, "shortcut_message")
        ensure_type(heal_room_message, str, "heal_room_message")
        ensure_type(boss_encounter_message, str, "boss_encounter_message")

        self.dungeon_name = name
        self.start_message = start_message
        self.shortcut_message = shortcut_message
        self.heal_room_message = heal_room_message
        self.boss_encounter_message = boss_encounter_message
        self.length = length
        self.special_dungeon = special_dungeon
        self.boss_enemy_id = boss_enemy_id
        self.enemy_set_id = enemy_set_id

    @property
    def boss(self) -> EnemyActor:
        from RPyG.content import ContentLibrary

        library = ContentLibrary.get_library()
        return library.enemies[self.boss_enemy_id]

    @property
    def enemy_set(self) -> EnemySet:
        from RPyG.content import ContentLibrary

        library = ContentLibrary.get_library()
        return library.enemy_sets[self.enemy_set_id]

    ## this function is a crime
    def traverse_dungeon(self) -> None:
        from RPyG import combat
        from RPyG.constructs import EnemyParty, RandomResultItem, RandomResultTable
        from RPyG.core_io import CoreIO, output_models
        from RPyG.game_state import GameState

        core_io = CoreIO.get_core_io()
        game_state = GameState.get_game_state()

        core_io.send_output(
            output_models.DungeonStartMessage(
                message=self.start_message,
                dungeon_name=self.dungeon_name,
            )
        )

        dungeon_table = RandomResultTable(
            [
                RandomResultItem(DungeonEvent.HEAL_ROOM, 0.167),
                RandomResultItem(DungeonEvent.SHORTCUT, 0.167),
                RandomResultItem(DungeonEvent.BATTLE_ENEMY, 0.167),
                RandomResultItem(DungeonEvent.NOTHING, 0.5),
            ]
        )
        if game_state.dungeon_progress is None:
            raise RuntimeError("Dungeon has not been properly loaded into GameState")
        while game_state.dungeon_progress < self.length:
            game_state.progress_dungeon(1)
            match dungeon_table.generate_result():
                case DungeonEvent.HEAL_ROOM:
                    core_io.send_output(
                        output_models.DungeonUpdateMessage(
                            event=output_models.DungeonUpdateMessage.HealRoomEvent(
                                message=self.heal_room_message
                            )
                        )
                    )
                    for member_instance in game_state.player_party.members:
                        member_instance.inventory.gain_potion(2)
                        member_instance.heal(60)
                case DungeonEvent.SHORTCUT:
                    game_state.progress_dungeon(2)
                    core_io.send_output(
                        output_models.DungeonUpdateMessage(
                            event=output_models.DungeonUpdateMessage.ShortcutEvent(
                                message=self.shortcut_message
                            )
                        )
                    )
                case DungeonEvent.BATTLE_ENEMY:
                    enemy_count = int(
                        len(game_state.player_party.members) + random.randint(-2, 2)
                    )
                    if enemy_count <= 0:
                        enemy_count = 1
                    enemy_party = self.enemy_set.generate_enemy_party(enemy_count)
                    core_io.send_output(
                        output_models.DungeonUpdateMessage(
                            event=output_models.DungeonUpdateMessage.EnemyEncounterEvent(
                                message=enemy_party.name
                            )
                        )
                    )

                    game_state.set_enemy_party(enemy_party)
                    combat.battle()
                    if len(game_state.player_party.members) == 0:
                        return
                case DungeonEvent.NOTHING:
                    core_io.send_output(output_models.EmptyDistanceMessage(distance=1))

        if len(game_state.player_party.members) != 0:
            core_io.send_output(
                output_models.DungeonUpdateMessage(
                    event=output_models.DungeonUpdateMessage.BossEncounterEvent(
                        message=self.boss_encounter_message
                    )
                )
            )
            game_state.set_enemy_party(
                EnemyParty(
                    self.boss.name,
                    [self.boss],
                )
            )
            combat.battle()
            if game_state.player_party.members == []:
                return

    def validate(self) -> bool:
        ensure_type(self.dungeon_name, str, "self.dungeon_name")
        ensure_type(self.start_message, str, "self.start_message")
        ensure_type(self.shortcut_message, str, "self.shortcut_message")
        ensure_type(self.heal_room_message, str, "self.heal_room_message")
        ensure_type(self.boss_encounter_message, str, "self.boss_encounter_message")
        ensure_type(self.boss_enemy_id, str, "self.boss_enemy_id")
        ensure_type(self.enemy_set_id, str, "self.enemy_set_id")
        ensure_type(self.length, int, "self.length")
        return True
