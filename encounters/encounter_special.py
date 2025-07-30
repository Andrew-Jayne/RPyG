import config

# Just for Type Checking
from actors import EnemyParty, PlayerParty
from actors.actor_enemy import Enemy
from combat import battle
from content.content import DUNGEONS_SPECIAL, ENEMIES_SPECIAL
from encounters.encounter_dungeon import Dungeon
from gameState.file import save_game
from interaction.interaction import Interaction
from message.message import Message
from utilites.utilities import ensure_type


class SpecialEncounters:
    @staticmethod
    def get_special_enemy(enemy_identifier) -> Enemy:
        enemy_attributes = ENEMIES_SPECIAL[enemy_identifier]

        return Enemy(**enemy_attributes)

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

        enemy_instance = __class__.get_special_enemy("midway_boss")
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
        dungeon_attributes = DUNGEONS_SPECIAL["algolons_fortess"]
        active_dungeon = Dungeon(dungeon_attributes)
        active_dungeon.travese_dungeon(player_party_instance)

    @staticmethod
    def penultimate_boss(player_party_instance: PlayerParty) -> None:
        ensure_type(player_party_instance, PlayerParty, "player_party_instance")

        enemy_instance = __class__.get_special_enemy("penultimate_boss")
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

        enemy_instance = __class__.get_special_enemy("ultimate_boss")
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
