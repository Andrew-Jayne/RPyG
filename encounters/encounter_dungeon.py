import random
import time
from typing import Any

import combat
import config
from actors import Enemy, EnemyParty, PlayerParty
from content.enemy_library import EnemySet
from utilites import ensure_type


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
        dungeon_name: str,
        messages: dict[str, str],
        length: int,
        enemies: list[dict[str, Any]],
        boss: dict[str, Any],
    ):
        ensure_type(dungeon_name, str, "dungeon_name")
        ensure_type(messages, dict, "messages")
        for messages_key, messages_value in messages.items():
            ensure_type(messages_key, str, "messages_key")
            ensure_type(messages_value, str, "messages_value")
        ensure_type(length, int, "length")
        ensure_type(enemies, list, "enemies")
        for enemies_item in enemies:
            ensure_type(enemies_item, dict, "enemies_item")
            for enemies_item_key in enemies_item.keys():
                ensure_type(enemies_item_key, str, "enemies_item_key")
        ensure_type(boss, dict, "boss")
        for boss_data_key in boss.keys():
            ensure_type(boss_data_key, str, "boss_data_key")

        self.dungeon_name = dungeon_name
        self.messages = DungeonMessages(**messages)
        self.length = length

        enemy_set_instances: list[EnemySet] = []
        for enemy_data in enemies:
            enemy_set_instances.append(EnemySet(**enemy_data))
        self.enemies = enemy_set_instances
        self.boss = Enemy(**boss)

    def travese_dungeon(self, player_party_instance: PlayerParty) -> bool:
        from message.message import Message

        ensure_type(player_party_instance, PlayerParty, "player_party_instance")
        dungeon_progress = 0
        Message.display_message(self.messages.start_message, 2)

        while dungeon_progress < self.length:
            dungeon_progress += 1
            if config.GLOBAL_GAME_MODE == "MANUAL":
                time.sleep(2)
            encouter_chance = random.randint(0, 5)
            match encouter_chance:
                case 0:
                    Message.display_message(self.messages.heal_room_message, 1)
                    for member_instance in player_party_instance.members:
                        member_instance.inventory.gain_potion(2)
                        member_instance.heal(20)
                case 1:
                    dungeon_progress += 2
                    Message.display_message(self.messages.shortcut_message, 1)
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
                    Message.encounter_message(enemy_party.name)
                    combat.battle(player_party_instance, enemy_party)
                    if len(player_party_instance.members) == 0:
                        return False
                case _:
                    Message.empty_travel_message(1)

        if len(player_party_instance.members) != 0:
            Message.display_message(self.messages.boss_encounter_message, 1)
            enemy_instance = self.boss
            combat.battle(
                player_party_instance,
                EnemyParty(
                    enemy_instance.name,
                    [enemy_instance],
                ),
            )
            if len(player_party_instance.members) != 0:
                Message.special_encounter_message(
                    player_party_instance.progress,
                    player_party_instance.name,
                    "success_messages",
                )
                return True
            else:
                Message.special_encounter_message(
                    player_party_instance.progress,
                    player_party_instance.name,
                    "failure_messages",
                )
                return False
        return False
