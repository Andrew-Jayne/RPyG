from typing import Any

import config

# Just for Type Checking
from actors import EnemyParty, PlayerParty
from actors.actor_enemy import Enemy
from combat import battle
from content.content import DUNGEONS, ENEMIES
from encounters.encounter_dungeon import Dungeon
from gameState.file import save_game
from interaction.interaction import Interaction
from message.message import Message
from utilites import ensure_type


class SpecialEncounters:
    @staticmethod
    def get_special_enemy(enemy_identifier: str) -> Enemy:
        from content.enemy_library import EnemyLibrary

        ensure_type(enemy_identifier, str, "enemy_identifier")
        ensure_type(ENEMIES, EnemyLibrary, "ENEMIES")
        if enemy_identifier not in ENEMIES.special_enemies.keys():
            raise FileNotFoundError(
                f"Unable to locate Enemy with ID: {enemy_identifier}"
            )
        return ENEMIES.special_enemies[enemy_identifier]

    @staticmethod
    def tavern_notice(player_party_instance: PlayerParty) -> None:
        ensure_type(player_party_instance, PlayerParty, "player_party_instance")

        Message.special_encounter_message(
            player_party_instance.progress, player_party_instance.name, "messages"
        )
        Interaction.embark()

    @staticmethod
    def friendly_keep_visit(player_party_instance: PlayerParty) -> None:
        ensure_type(player_party_instance, PlayerParty, "player_party_instance")

        keep_visit_message = f"{player_party_instance.name} is welcomed at the Open Hall by King Stallman"

        Message.display_message(keep_visit_message, 1)
        Message.special_encounter_message(
            player_party_instance.progress, player_party_instance.name, "messages"
        )
        Interaction.accept_quest()
        for member_instance in player_party_instance.members:
            member_instance.heal(300)
            member_instance.inventory.gain_potion(9)

        keep_depart_message = f"{player_party_instance.name} is are fully rested and have a full stock of potions"
        Message.display_message(keep_depart_message, 2)

    @staticmethod
    def midway_boss(player_party_instance: PlayerParty) -> None:
        ensure_type(player_party_instance, PlayerParty, "player_party_instance")

        enemy_instance = SpecialEncounters.get_special_enemy("midway_boss")
        Message.special_encounter_message(
            player_party_instance.progress, player_party_instance.name, "messages"
        )
        enemy_party = EnemyParty(enemy_instance.name, [enemy_instance])
        battle(player_party_instance, enemy_party)
        if len(player_party_instance.members) != 0:
            Message.special_encounter_message(
                player_party_instance.progress,
                player_party_instance.name,
                "success_messages",
            )
        else:
            Message.special_encounter_message(
                player_party_instance.progress,
                player_party_instance.name,
                "failure_messages",
            )

    @staticmethod
    def enemy_keep_visit(player_party_instance: PlayerParty) -> None:
        Message.special_encounter_message(
            player_party_instance.progress, player_party_instance.name, "messages"
        )
        if "algolons_fortress" not in DUNGEONS.special_dungeons.keys():
            raise FileNotFoundError(
                f"Unable to locate Dungeon with the ID algolons_fortress, avalible IDs are {DUNGEONS.special_dungeons.keys()}"
            )
        active_dungeon: Dungeon = DUNGEONS.special_dungeons["algolons_fortress"]
        active_dungeon.travese_dungeon(player_party_instance)

    @staticmethod
    def penultimate_boss(player_party_instance: PlayerParty) -> None:
        ensure_type(player_party_instance, PlayerParty, "player_party_instance")

        enemy_instance = SpecialEncounters.get_special_enemy("penultimate_boss")
        Message.display_message(f"Your Party Battles {enemy_instance.name}!", 1)
        enemy_party = EnemyParty(enemy_instance.name, [enemy_instance])
        battle(player_party_instance, enemy_party)
        if len(player_party_instance.members) != 0:
            Message.special_encounter_message(
                player_party_instance.progress,
                player_party_instance.name,
                "success_messages",
            )
        else:
            Message.special_encounter_message(
                player_party_instance.progress,
                player_party_instance.name,
                "failure_messages",
            )

    @staticmethod
    def final_boss(player_party_instance: PlayerParty) -> None:
        ensure_type(player_party_instance, PlayerParty, "player_party_instance")

        enemy_instance = SpecialEncounters.get_special_enemy("ultimate_boss")
        Message.display_message(f"Your Party must now battle {enemy_instance.name}!", 1)
        enemy_party = EnemyParty(enemy_instance.name, [enemy_instance])
        battle(player_party_instance, enemy_party)
        if len(player_party_instance.members) != 0:
            Message.special_encounter_message(
                player_party_instance.progress,
                player_party_instance.name,
                "success_messages",
            )
            end_game_message = f"""
Fortranus the Ancient One has been Vanquished at the hands of {player_party_instance.name}


Your adventure has been completed, you may start a new adventure if you so choose
"""

            Message.display_message(end_game_message, 2)
            if config.GLOBAL_GAME_MODE == "MANUAL":
                save_game(player_party_instance)
