import random
from typing import TYPE_CHECKING

from RPyG import combat
from RPyG.actors import EnemyParty, PlayerParty
from RPyG.constructs import EnemySet
from RPyG.utilities import ensure_type


if TYPE_CHECKING is True:
    from RPyG.actors import Enemy


class Dungeon:
    dungeon_name: str
    start_message: str
    shortcut_message: str
    heal_room_message: str
    boss_encounter_message: str
    boss_enemy_id: str
    enemy_set_id: str
    length: int

    def __init__(
        self,
        kind: str,
        name: str,
        length: int,
        boss_enemy_id: str,
        enemy_set_id: str,
        start_message: str,
        shortcut_message: str,
        heal_room_message: str,
        boss_encounter_message: str,
    ):
        self.dungeon_name = name
        self.start_message = start_message
        self.shortcut_message = shortcut_message
        self.heal_room_message = heal_room_message
        self.boss_encounter_message = boss_encounter_message
        self.length = length
        self.boss_enemy_id = boss_enemy_id
        self.enemy_set_id = enemy_set_id

    @property
    def boss(self) -> Enemy:
        from RPyG.content import ContentLibrary

        library = ContentLibrary.get_library()
        return library.enemies[self.boss_enemy_id]

    @property
    def enemy_set(self) -> EnemySet:
        from RPyG.content import ContentLibrary

        library = ContentLibrary.get_library()
        return library.enemy_sets[self.enemy_set_id]

    ## this function is a crime
    def traverse_dungeon(self, player_party_instance: PlayerParty) -> None:
        from RPyG.core_io import CoreIO
        from RPyG.core_io.io_models import EmptyDistanceMessage, OutputMessage

        core_io = CoreIO.get_core_io()
        ensure_type(player_party_instance, PlayerParty, "player_party_instance")

        # this allows saving and resuming inside of dungeons
        player_party_instance.in_dungeon = True
        player_party_instance.active_dungeon = self
        player_party_instance.dungeon_progress = 0

        core_io.send_output(OutputMessage(self.start_message))

        while player_party_instance.dungeon_progress < self.length:
            player_party_instance.dungeon_progress += 1
            encouter_chance = random.randint(0, 5)
            match encouter_chance:
                case 0:
                    core_io.send_output(OutputMessage(self.heal_room_message))
                    for member_instance in player_party_instance.members:
                        member_instance.inventory.gain_potion(2)
                        member_instance.heal(60)
                case 1:
                    player_party_instance.dungeon_progress += 2
                    core_io.send_output(OutputMessage(self.shortcut_message))
                case 4:
                    enemy_count = int(
                        len(player_party_instance.members) + random.randint(-2, 2)
                    )
                    if enemy_count == 0:
                        enemy_count = 1
                    enemy_party = self.enemy_set.generate_enemy_party(enemy_count)
                    core_io.send_output(
                        OutputMessage(f"Your Party encounters a {enemy_party.name}!")
                    )
                    combat.battle(player_party_instance, enemy_party)
                    if len(player_party_instance.members) == 0:
                        return
                case _:
                    core_io.send_output(EmptyDistanceMessage(distance=1))

        if len(player_party_instance.members) != 0:
            core_io.send_output(OutputMessage(self.boss_encounter_message))
            enemy_instance = self.boss
            combat.battle(
                player_party_instance,
                EnemyParty(
                    enemy_instance.name,
                    [enemy_instance],
                ),
            )
        player_party_instance.in_dungeon = False
        player_party_instance.active_dungeon = None
        player_party_instance.dungeon_progress = 0

    def validate(self) -> bool:
        _var = self
        return True
