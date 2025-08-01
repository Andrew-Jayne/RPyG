import textwrap
import time

import config

# Only used for Type checking/Hinting
from actors import EnemyParty, PlayerParty
from actors.actor_combatant import Combatant
from actors.actor_playable import PlayableActor
from utilites import ensure_type
from content.content import STORY


class Message:
    @staticmethod
    def display_message(message: str, new_line_count: int) -> None:
        """
        Use this function rather than local 'print()' in functions.
        This does basic processing for optimal display and will allow for better output handling when the UI is redone.
        """
        ending = "\n" * new_line_count
        wrapped_message = ""

        # Split the message into lines to handle them individually
        lines = message.split("\n")
        for line in lines:
            # Apply text wrapping to each line individually
            wrapped_line = textwrap.fill(line, width=80)
            wrapped_message += wrapped_line + "\n"

        # Print the final wrapped message, removing the last added newline and adding the custom ending
        print(wrapped_message.rstrip("\n"), end=ending)

    # Actor Messages
    @staticmethod
    def defeated_message(name: str) -> None:
        defeated_message = f"{name} has been defeated"

        __class__.display_message(defeated_message, 2)

    @staticmethod
    def encounter_message(group_name: str) -> None:
        encounter_message = f"Your Party encounters a {group_name}!"

        __class__.display_message(encounter_message, 2)

    @staticmethod
    def actor_health_message(actor_instance: Combatant) -> None:
        ensure_type(actor_instance, Combatant, "actor_instance")

        actor_health_message = (
            f"{actor_instance.name} has {actor_instance.health} Health remaining"
        )

        __class__.display_message(actor_health_message, 2)

    @staticmethod
    def actor_attack_message(attacker_instance: Combatant, damage_value: int) -> None:
        ensure_type(attacker_instance, Combatant, "actor_instance")

        if (
            config.GLOBAL_GAME_MODE == "MANUAL"
            and isinstance(attacker_instance, PlayableActor) is False
        ):
            time.sleep(2)

        actor_attack_message = f"{attacker_instance.name} attacks with {attacker_instance.attack_name} inflicting {damage_value} damage"

        __class__.display_message(actor_attack_message, 2)

    @staticmethod
    def actor_critical_attack_message(
        attacker_instance: Combatant, damage_value: int
    ) -> None:
        ensure_type(attacker_instance, Combatant, "actor_instance")

        if (
            config.GLOBAL_GAME_MODE == "MANUAL"
            and isinstance(attacker_instance, PlayableActor) is False
        ):
            time.sleep(2)

        actor_critical_attack_message = f"""
{attacker_instance.name} attacks with {attacker_instance.attack_name} inflicting {damage_value * 2} damage
{attacker_instance.name} got a critical hit!!
"""
        __class__.display_message(actor_critical_attack_message, 2)

    # Battle Messages
    @staticmethod
    def battle_hud_message(
        player_party_instance: PlayerParty, enemy_party_instance: EnemyParty
    ) -> None:
        ensure_type(player_party_instance, PlayerParty, "player_party_instance")
        ensure_type(enemy_party_instance, EnemyParty, "enemy_party_instance")

        battle_hud_message = ""

        for playable_instance in player_party_instance.members:
            battle_hud_message += (
                f"{playable_instance.name}: {playable_instance.health}"
            )
            battle_hud_message += "\n"
        battle_hud_message += "\n"

        for enemy_instance in enemy_party_instance.members:
            battle_hud_message += f"{enemy_instance.name}: {enemy_instance.health}\n"
            battle_hud_message += "\n"

        __class__.display_message(battle_hud_message, 2)

    @staticmethod
    def battle_start_message() -> None:
        battle_start_message = "The Battle Begins!"

        __class__.display_message(battle_start_message, 3)

    # Encounter Messages
    @staticmethod
    def distance_since_last(no_encounters_since: int) -> None:
        distance_since_last_message = (
            f"After {no_encounters_since * 10} miles of travel"
        )

        __class__.display_message(distance_since_last_message, 1)

    @staticmethod
    def flee_failure_message(player_name: str, enemy_name: str) -> None:
        flee_failure_message = f"{player_name} has Failed to Escape the {enemy_name}!"

        if config.GLOBAL_GAME_MODE == "MANUAL":
            time.sleep(2)

        __class__.display_message(flee_failure_message, 1)

    @staticmethod
    def flee_success_message(player_name: str, enemy_name: str) -> None:
        flee_success_message = (
            f"{player_name} has Successfully Escaped the {enemy_name}!"
        )

        __class__.display_message(flee_success_message, 1)

    @staticmethod
    def special_encounter_message(
        progress_value: int, party_name: str, message_type: str
    ) -> None:
        if message_type not in ["messages", "success_messages", "failure_messages"]:
            raise ValueError(
                'Message type must be one of ["messages", "success_messages", "failure_messages"]'
            )

        all_events = STORY["progress_events"]

        current_event = all_events[str(progress_value)]
        for message in current_event[message_type]:
            formatted_message = message.format(party_name=party_name)

            __class__.display_message(formatted_message, 2)
            if config.GLOBAL_GAME_MODE == "MANUAL":
                time.sleep(2)

    # Player Messages
    @staticmethod
    def post_game_recap(player_party_instance: PlayerParty) -> None:
        ensure_type(player_party_instance, PlayerParty, "player_party_instance")

        for player_instance in player_party_instance.members:
            player_report = f"""
Player Name: {player_instance.name}
Player Base Health: {player_instance.base_health}                             
Player Final Health: {player_instance.health}
Player Int: {player_instance.intellect}
Player Str: {player_instance.strength}
Player Agl: {player_instance.agility}
Player Lck: {player_instance.luck}
Player Gold: {player_instance.inventory.gold}
Player Potions: {player_instance.inventory.potions}
Player Attack Name: {player_instance.attack_name}
Player Attack Power: {player_instance.attack_power}
"""

            __class__.display_message(player_report, 2)

        __class__.display_message("Fallen Members", 2)

        for player_instance in player_party_instance.dead_members:
            player_report = f"""
Player Name: {player_instance.name}
Player Base Health: {player_instance.base_health}                             
Player Final Health: {player_instance.health}
Player Int: {player_instance.intellect}
Player Str: {player_instance.strength}
Player Agl: {player_instance.agility}
Player Lck: {player_instance.luck}
Player Gold: {player_instance.inventory.gold}
Player Potions: {player_instance.inventory.potions}
Player Attack Name: {player_instance.attack_name}
Player Attack Power: {player_instance.attack_power}
"""

            __class__.display_message(player_report, 2)

    @staticmethod
    def game_over_message(player_party_instance: PlayerParty) -> None:
        game_over_message = f"{player_party_instance.name} has failed in their quest after {player_party_instance.progress * 10} miles"

        __class__.display_message(game_over_message, 2)
        time.sleep(2)
        __class__.post_game_recap(player_party_instance)

    @staticmethod
    def empty_travel_message(empty_distance: int) -> None:
        if config.GLOBAL_GAME_MODE == "MANUAL":
            time.sleep(2)
        empty_travel_message = f"{'.' * (empty_distance - 1)}"

        __class__.display_message(empty_travel_message, 1)
