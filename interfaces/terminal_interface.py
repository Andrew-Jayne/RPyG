from typing import Any

from RPyG.core_io import RPyGInterface, OutputMessage, InputRequest
from RPyG.utilites import ensure_type


## Monkas this file is huge lol

class BasicTerminalInterface(RPyGInterface):
    input_buffer: dict[str, Any]

    def __init__(self):
        super().__init__()
        self.input_buffer = {}

    def show_ouput(self, output_data: OutputMessage) -> None:
        return print(output_data)

    def request_input(self, request: InputRequest) -> None:
        self.input_buffer = {"data": input(str(request.messages))}

    def receive_input(self) -> dict:
        data = self.input_buffer.get("data")
        if data is None:
            raise RuntimeError(
                "Input buffer is empty, did you call request_input before calling receive_input"
            )
        # reset buffer
        self.input_buffer = {}
        return data

    @staticmethod
    def sanitize(input_string: str, max_length: int = 32) -> str:
        """
        This function Sanitizes strings passed into it and returns up to the max length chars (Default is 32)
        With most escape sequences and control chars removed

        Will raise ValueError if a string exceeding 512 chars is passed
        """
        # raise ValueError if string is longer than 512 Chars
        if len(input_string) > 512:
            raise ValueError("Input Length Exceeds Expected Parameters: Exiting!")
        # Set unwanted chars
        chars_to_remove = (
            r"!#*"  # Basic symbols
            r".[]{}"  # Brackets
            r"\\|\":;"  # Escaped stuff
            r"/<>\\()"  # Slashes and parens
            r"'"  # Final single quote
        )
        control_chars = "".join(map(chr, range(0, 32))) + chr(127)
        literal_control_strings = [
            "\\n",
            "\\t",
            "\\r",
            "\\x0c",
            "\\x0b",
        ]  # Literal string representations of control chars
        # Remove unwanted chars
        limited_string = input_string[
            :max_length
        ]  # Limit the input to the desired length
        for literal in literal_control_strings:
            limited_string = limited_string.replace(literal, "")
        cleaned_string = "".join(
            char
            for char in limited_string
            if char not in chars_to_remove and char not in control_chars
        )

        return cleaned_string

    def validate_input(self, choice_list: list[str]) -> str:
        """
        Checks that the string input by the user is in the allowed list of responses
        Sanitizes the input then returns up to the max length specified
        """
        options_list = "\n".join(choice_list)
        chosen_action = ""
        dumb_check = 0
        while chosen_action not in choice_list:
            chosen_action = self.sanitize(input("").upper())
            if chosen_action not in choice_list:
                self.show_ouput(
                    "That is not a Valid Option. Try again, valid options are", 2
                )
                self.show_ouput(options_list, 1)
                dumb_check += 1
                if dumb_check == 10:
                    raise FileNotFoundError(
                        "Look it's not hard, just enter a valid choice...."
                    )
        return chosen_action

    def custom_text_entry(
        self,
        input_messages: list[str],
        max_length: int,
    ) -> str:
        for message in input_messages:
            self.show_ouput(message, 1)
        return self.sanitize(input()[:max_length])

    def prompt_user(
        self,
        options: list[str],
        base_messages: list[str],
        *,
        return_index: bool = False,
    ) -> str:
        ensure_type(options, list, "options")
        ensure_type(base_messages, list, "base_messages")

        formatted_message = ""
        for message in base_messages:
            formatted_message += f"{message}\n"

        for option in options:
            formatted_message += f"{option}\n"

        self.show_ouput(formatted_message, 1)

        if return_index is True:
            int_options: list[str]
            int_options = []
            for i in range(len(options) + 1):
                int_options.append(str(i))
            options = int_options

        response = self.validate_input(options)
        return response


#### logic that is interface data that has been expunged from the program itself

    ## from New game
    config = Config.get_config()
    match game_mode:
        case "AUTO":
            config.global_game_mode = "AUTO"
            return PlayerParty(name="The Default Party", members=default_party())
        case "MANUAL":
            config.global_game_mode = "MANUAL"
            if using_default_party is True:
                return PlayerParty(name="The Default Party", members=default_party())
            else:
                
        case _:
            raise ValueError("Error No Valid Game Mode was selected")




# This module is for static, or single update constants, this allows values to be avalible without class or module imports
# This is a default value that should be can be updated to "MANUAL" during the welcome function


from typing import Literal, Self


class Config:
    _instance: Self | None = None  # Class variable with = None
    _global_game_mode: Literal["AUTO", "MANUAL"] = "AUTO"
    _debug_enabled: bool = False

    def __init__(
        self, global_game_mode: Literal["AUTO", "MANUAL"], debug_enabled: bool
    ):
        if Config._instance is None:
            Config._global_game_mode = global_game_mode
            Config._debug_enabled = debug_enabled
            Config._instance = self
        print("initied config")

    @property
    def global_game_mode(self) -> Literal["AUTO", "MANUAL"]:
        return self._global_game_mode

    @global_game_mode.setter
    def global_game_mode(self, mode: Literal["AUTO", "MANUAL"]) -> None:
        if mode not in ["AUTO", "MANUAL"]:
            raise ValueError(
                f"Mode: {mode} is not a valid option for global_game_mode must be either 'AUTO' or 'MANUAL'"
            )
        self._global_game_mode = mode

    @property
    def debug_enabled(self) -> bool:
        return self._debug_enabled

    @debug_enabled.setter
    def debug_enabled(self, mode: bool) -> None:
        match mode:
            case False:
                self._debug_enabled = False
            case True:
                self._debug_enabled = True
            case _:
                raise ValueError(f"Invalid Option for Debug Enabled {mode}")

    @classmethod
    def get_config(cls):
        if Config._instance is not None:
            return Config._instance
        else:
            raise RuntimeError(
                "Attempted to access Config instance before initialization"
            )



import random

from RPyG.actors import CombatantParty, PlayableActor, PlayerParty

# Only Used For Type Hinting/Checking
from RPyG.message.message import Message
from RPyG.utilites import ensure_type


# Interaction Function Guidelines
# Functions should return either a string or an int, the upstream functions will handle logic based on the items passed
# Adding the str to bool logic here just adds bloat and over-complicates very, very simple functions


class Interaction:
    @staticmethod
    def choose_combat_target(target_party_instance: CombatantParty) -> int:
        ensure_type(target_party_instance, CombatantParty, "target_party_instance")
        target_options: list[str]
        target_options = []
        from RPyG.config import Config

        config = Config.get_config()
        match config.global_game_mode:
            case "AUTO":
                # need to move this up stream later and/or merge interaction inside playable actor pepeW
                return target_party_instance.members[0].select_combat_target(
                    target_party_instance
                )
            case "MANUAL":
                for i, member in enumerate(target_party_instance.members):
                    target_options.append(f"{i} {member.name}:{member.health}")

                target_messages = [
                    "Which enemy will you attack?",
                ]

                return int(
                    Interaction.prompt_user(
                        target_options, target_messages, return_index=True
                    )
                )
            case _:
                raise ValueError("Invalid Game mode")

    @staticmethod
    def encounter_enemy() -> str:
        from RPyG.config import Config

        config = Config.get_config()
        match config.global_game_mode:
            case "AUTO":
                chosen_action = random.choice(["FLEE", "ATTACK"])
                return chosen_action
            case "MANUAL":
                encounter_options = ["BATTLE", "FLEE"]
                encounter_message = ["Choose an Action:"]
                return Interaction.prompt_user(encounter_options, encounter_message)
            case _:
                return "ATTACK"

    @staticmethod
    def post_battle(player_party_instance: PlayerParty) -> str:
        ensure_type(player_party_instance, PlayerParty, "player_party_instance")
        from RPyG.config import Config

        config = Config.get_config()

        match config.global_game_mode:
            case "AUTO":
                for player_instance in player_party_instance.members:
                    if (
                        player_instance.health < 20
                        and player_instance.inventory.potions != 0
                    ):
                        return "HEAL"
                return "TRAVEL"

            case "MANUAL":
                post_battle_options = ["HEAL", "TRAVEL", "SAVE"]
                post_battle_message = ["Choose an Action:"]
                return Interaction.prompt_user(post_battle_options, post_battle_message)
            case _:
                return "TRAVEL"

    @staticmethod
    def in_battle(player_instance: PlayableActor) -> str:
        ensure_type(player_instance, PlayableActor, "player_instance")
        from RPyG.config import Config

        config = Config.get_config()

        match config.global_game_mode:
            case "AUTO":
                if (
                    player_instance.health <= 40
                    and player_instance.inventory.potions != 0
                ):
                    chosen_action = "HEAL"
                elif player_instance.inventory.potions == 0:
                    Message.display_message(
                        f"{player_instance.name} has no remaining potions and must make a stand!",
                        1,
                    )
                    chosen_action = "ATTACK"
                else:
                    chosen_action = random.choice(
                        [player_instance.react_action, "ATTACK", "ATTACK", "ATTACK"]
                    )

                return chosen_action
            case "MANUAL":
                battle_options = [
                    "ATTACK",
                    f"{player_instance.special_attack_name}",
                    f"{player_instance.react_action}",
                    "HEAL",
                ]
                battle_messages = [f"{player_instance.name}", "Choose an Action:"]

                battle_choice = Interaction.prompt_user(battle_options, battle_messages)
                if (
                    battle_choice == "HEAL"
                    and player_instance.is_fully_healed() is True
                ):
                    Message.display_message(
                        f"{player_instance.name} is fully healed, it would be unwise to use a potion",
                        1,
                    )
                battle_choice = Interaction.prompt_user(battle_options, battle_messages)
                if battle_choice == "HEAL":
                    Message.display_message(
                        "Stubborn aren't you, fine waste the damn potion", 1
                    )

                return battle_choice
            case _:
                return "ATTACK"

    @staticmethod
    def at_merchant(player_party_instance: PlayerParty) -> None:
        import math

        ensure_type(player_party_instance, PlayerParty, "player_party_instance")
        from RPyG.config import Config

        config = Config.get_config()

        Message.display_message("You arrive at a merchant", 1)
        match config.global_game_mode:
            case "AUTO":
                # init Counts
                player_count = 0
                gold_spent = 0
                potions_sold = 0

                for player_instance in player_party_instance.members:
                    player_count += 1
                    while (
                        player_instance.inventory.potions < 100
                        and player_instance.inventory.gold != 0
                    ):
                        if player_instance.inventory.spend_gold(25) is True:
                            gold_spent += 25

                            player_instance.inventory.gain_potion(1)
                            potions_sold += 1

                            Message.display_message(
                                f"{player_instance.name} purchases a potion. They now have {player_instance.inventory.potions}",
                                1,
                            )
                        else:
                            Message.display_message(
                                f"{player_instance.name} does not have enough Gold to purchase more potions",
                                1,
                            )
                            break
            case "MANUAL":
                player_choice = None
                merchant_options = ["BUY", "LEAVE", "BUY MAX"]

                for player_instance in player_party_instance.members:
                    merchant_messages = [
                        f"{player_instance.name}",
                        f"Gold: {player_instance.inventory.gold}",
                        f"Potions: {player_instance.inventory.potions}",
                        "",
                        "Choose an Action:",
                    ]

                    while player_choice != "LEAVE":
                        player_choice = Interaction.prompt_user(
                            merchant_options, merchant_messages
                        )
                        Message.display_message(
                            f"{player_instance.name} has {player_instance.inventory.potions} potions & {player_instance.inventory.gold} gold",
                            1,
                        )
                        match player_choice:
                            case "BUY":
                                if player_instance.inventory.spend_gold(25) is True:
                                    player_instance.inventory.gain_potion(1)
                                    Message.display_message(
                                        f"{player_instance.name} purchases a potion. They now have {player_instance.inventory.potions} & {player_instance.inventory.gold} gold",
                                        1,
                                    )
                                else:
                                    Message.display_message(
                                        f"{player_instance.name} does not have enough Gold to purchase more potions",
                                        1,
                                    )
                                    player_choice = "LEAVE"
                            case "BUY MAX":
                                # Using floor to make sure you can't buy 10 potions with 245 gold
                                rounds = math.floor(player_instance.inventory.gold / 25)
                                player_instance.inventory.spend_gold((rounds * 25))
                                player_instance.inventory.gain_potion(rounds)
                                player_choice = "LEAVE"
                            case "LEAVE":
                                player_choice = "LEAVE"
                            case _:
                                player_choice = "LEAVE"

            case _:
                raise ValueError("invalid game mode")

    @staticmethod
    def confirm_rest() -> bool:
        from RPyG.config import Config

        config = Config.get_config()
        match config.global_game_mode:
            case "AUTO":
                return random.choice([True, True, False])
            case "MANUAL":
                rest_options = ["YES", "NO"]
                rest_message = ["Will you Rest here?:"]
                rest_choice = Interaction.prompt_user(rest_options, rest_message)
                if rest_choice == "YES":
                    return True
                if rest_choice == "NO":
                    return False
                return False
            case _:
                raise ValueError("invalid game mode")

    @staticmethod
    def mystery_action() -> str:
        from RPyG.config import Config

        config = Config.get_config()
        match config.global_game_mode:
            case "AUTO":
                return random.choice(["GREET", "GREET", "ATTACK"])
            case "MANUAL":
                rest_options = ["ATTACK", "GREET"]
                rest_message = ["What do you do?:"]
                return Interaction.prompt_user(rest_options, rest_message)
            case _:
                raise ValueError("invalid game mode")

    @staticmethod
    def loot_action() -> str:
        from RPyG.config import Config

        config = Config.get_config()
        match config.global_game_mode:
            case "AUTO":
                return random.choice(["OPEN", "OPEN", "LEAVE"])
            case "MANUAL":
                rest_options = ["OPEN", "LEAVE"]
                rest_message = ["What do you do?:"]
                return Interaction.prompt_user(rest_options, rest_message)
            case _:
                raise ValueError("invalid game mode")

    @staticmethod
    def embark() -> bool:
        from RPyG.config import Config

        config = Config.get_config()
        match config.global_game_mode:
            case "AUTO":
                return True
            case "MANUAL":
                embark_options = ["EMBARK", "DRINK"]
                embark_options_message = ["What shall the party do?"]
                player_choice = Interaction.prompt_user(
                    embark_options, embark_options_message
                )

                while player_choice != "EMBARK":
                    player_choice = Interaction.prompt_user(
                        embark_options, embark_options_message
                    )

                    match player_choice:
                        case "EMBARK":
                            return True
                        case "DRINK":
                            Message.display_message(
                                "After many drinks, the kings missive sticks in your mind.",
                                1,
                            )
                        case _:
                            return True
                return True
            case _:
                raise ValueError("invalid game mode")
        return True

    @staticmethod
    def accept_quest() -> bool:
        from RPyG.config import Config

        config = Config.get_config()
        match config.global_game_mode:
            case "AUTO":
                return True
            case "MANUAL":
                quest_options = ["ACCEPT", "DECLINE"]
                quest_message = ["Will you accept this quest from the King?"]
                player_choice = Interaction.prompt_user(quest_options, quest_message)

                while player_choice != "ACCEPT":
                    player_choice = Interaction.prompt_user(
                        quest_options, quest_message
                    )
                    match player_choice:
                        case "ACCEPT":
                            return True
                        case "DECLINE":
                            Message.display_message(
                                "The King insists, and asks again", 1
                            )
                        case _:
                            return True
                return True
            case _:
                raise ValueError("invalid game mode")

        return True



import textwrap
import time

from RPyG.actors import Combatant, EnemyParty, PlayableActor, PlayerParty

# Only used for Type checking/Hinting
from RPyG.utilites import ensure_type


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
        from RPyG.config import Config

        config = Config.get_config()

        if (
            config.global_game_mode == "MANUAL"
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
        from RPyG.config import Config

        config = Config.get_config()

        if (
            config.global_game_mode == "MANUAL"
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
        from RPyG.config import Config

        config = Config.get_config()

        if config.global_game_mode == "MANUAL":
            time.sleep(2)

        __class__.display_message(flee_failure_message, 1)

    @staticmethod
    def flee_success_message(player_name: str, enemy_name: str) -> None:
        flee_success_message = (
            f"{player_name} has Successfully Escaped the {enemy_name}!"
        )

        __class__.display_message(flee_success_message, 1)

    @staticmethod
    # TODO This function gives me the ick, and sucks
    def special_encounter_message(
        progress_value: int,
        party_name: str,
        message_type: str,
    ) -> None:
        def show_message(message: str) -> None:
            formatted_message = message.format(party_name=party_name)
            from RPyG.config import Config

            config = Config.get_config()

            __class__.display_message(formatted_message, 2)
            if config.global_game_mode == "MANUAL":
                time.sleep(2)

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
        from RPyG.config import Config

        config = Config.get_config()
        if config.global_game_mode == "MANUAL":
            time.sleep(2)
        empty_travel_message = f"{'.' * (empty_distance - 1)}"

        __class__.display_message(empty_travel_message, 1)
