import random
from typing import Any

from RPyG import combat
from RPyG.actors import Enemy, EnemyParty, PlayerParty
from RPyG.constructs import EnemySet
from RPyG.core_io import CoreIO
from RPyG.core_io.io_models import EmptyDistanceMessage, OutputMessage
from RPyG.utilites import ensure_type


class DungeonMessages:
    start_message: str
    boss_encounter_message: str
    shortcut_message: str
    heal_room_message: str

    def __init__(
        self,
        start_message: str,
        boss_encounter_message: str,
        shortcut_message: str,
        heal_room_message: str,
    ):
        ensure_type(start_message, str, "start_message")
        ensure_type(boss_encounter_message, str, "boss_encounter_message")
        ensure_type(shortcut_message, str, "shortcut_message")
        ensure_type(heal_room_message, str, "heal_room_message")

        self.start_message = start_message
        self.boss_encounter_message = boss_encounter_message
        self.shortcut_message = shortcut_message
        self.heal_room_message = heal_room_message


class Dungeon:
    dungeon_name: str
    messages: DungeonMessages
    length: int
    enemies: list[EnemySet]
    boss: Enemy

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
        self.messages = DungeonMessages(
            start_message=start_message,
            shortcut_message=shortcut_message,
            heal_room_message=heal_room_message,
            boss_encounter_message=boss_encounter_message,
        )
        self.length = length

        # self.enemies = EnemySet(**enemy_sets_data)
        self.boss = ""

    ## this function is a crime
    def travese_dungeon(self, player_party_instance: PlayerParty) -> bool:
        core_io = CoreIO.get_core_io()
        ensure_type(player_party_instance, PlayerParty, "player_party_instance")
        dungeon_progress = 0
        core_io.send_output(OutputMessage(self.messages.start_message))

        while dungeon_progress < self.length:
            dungeon_progress += 1
            encouter_chance = random.randint(0, 5)
            match encouter_chance:
                case 0:
                    core_io.send_output(OutputMessage(self.messages.heal_room_message))
                    for member_instance in player_party_instance.members:
                        member_instance.inventory.gain_potion(2)
                        member_instance.heal(20)
                case 1:
                    dungeon_progress += 2
                    core_io.send_output(OutputMessage(self.messages.shortcut_message))
                case 4:
                    enemy_count = int(
                        len(player_party_instance.members) + random.randint(-2, 2)
                    )
                    if enemy_count == 0:
                        enemy_count = 1
                    chosen_enemy: dict = random.choice(self.enemies)
                    enemy_party = EnemySet.generate_enemy_party(
                        chosen_enemy, enemy_count
                    )
                    core_io.send_output(
                        {"messages": f"Your Party encounters a {enemy_party.name}!"}
                    )
                    combat.battle(player_party_instance, enemy_party)
                    if len(player_party_instance.members) == 0:
                        return False
                case _:
                    core_io.send_output(EmptyDistanceMessage(distance=1))

        ## THis is horrendus and I hate it
        def send_special_encounter_message(
            progress_value: int,
            party_name: str,
            message_type: str,
        ) -> None:
            def show_message(message: str) -> None:
                core_io = CoreIO.get_core_io()

                core_io.send_output(
                    OutputMessage(message.format(party_name=party_name))
                )

            from RPyG.content import ContentLibrary

            content_library: ContentLibrary = ContentLibrary.get_library()

            current_event = content_library.story_events[progress_value]
            match message_type:
                case "messages":
                    for message in current_event.messages:
                        show_message(message)
                case "success_messages":
                    for message in current_event.success_messages:
                        show_message(message)
                case "failure_messages":
                    for message in current_event.failure_messages:
                        show_message(message)
                case _:
                    raise ValueError(
                        'Message type must be one of ["messages", "success_messages", "failure_messages"]'
                    )

        if len(player_party_instance.members) != 0:
            core_io.send_output(OutputMessage(self.messages.boss_encounter_message))
            enemy_instance = self.boss
            combat.battle(
                player_party_instance,
                EnemyParty(
                    enemy_instance.name,
                    [enemy_instance],
                ),
            )
            if len(player_party_instance.members) != 0:
                send_special_encounter_message(
                    player_party_instance.progress,
                    player_party_instance.name,
                    "success_messages",
                )
                return True
            else:
                send_special_encounter_message(
                    player_party_instance.progress,
                    player_party_instance.name,
                    "failure_messages",
                )

                return False
        return False
