import os
import textwrap
from typing import Literal, cast

from RPyG import (
    CustomTextRequest,
    InputRequest,
    OutputMessage,
    RPyGInterface,
    UIElement,
    UserPromptRequest,
)
from RPyG.actors import PlayableActor
from RPyG.utilities import ensure_type


welcome_message = """
             This game looks best with a width of at least 80.
            If the next line is split please widen your terminal.
----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----

             NOTE: All Prompts in this game are case insensitive

"""


class BasicTerminalInterface(RPyGInterface):
    input_buffer: str
    game_mode: Literal["AUTO", "MANUAL"] = "MANUAL"

    def __init__(self, game_mode: Literal["AUTO", "MANUAL"]):
        RPyGInterface.__init__(self)
        self.input_buffer = ""
        self.game_mode = game_mode
        self.show_ouput(OutputMessage(welcome_message))

    def show_ouput(self, output: OutputMessage) -> None:
        ending = "\n"
        wrapped_message = ""

        # Split the message into lines to handle them individually
        lines = output.message.split("\n")
        for line in lines:
            # Apply text wrapping to each line individually
            wrapped_line = textwrap.fill(line, width=80)
            wrapped_message += wrapped_line + "\n"

        # Print the final wrapped message, removing the last added newline and adding the custom ending
        print(wrapped_message.rstrip("\n"), end=ending)

    def request_input(self, request: InputRequest) -> None:
        ensure_type(request, InputRequest, "request")
        match type(request).__name__:
            case "InputRequest":
                raise NotImplementedError
            case "UserPromptRequest":
                prompt_request = cast(UserPromptRequest, request)
                displayable_options = []
                for item in prompt_request.options:
                    if item is not None:
                        displayable_options.append(item)
                content = self.prompt_user(
                    options=displayable_options,
                    prompts=prompt_request.prompts,
                )

            case "CustomTextRequest":
                text_request = cast(CustomTextRequest, request)
                content = self.custom_text_entry(
                    text_request.prompts,
                    text_request.max_length,
                )
            case _:
                raise ValueError(
                    f"Got Unknown Child class of InputRequest {type(request).__name__}"
                )

        self.input_buffer = content

    def receive_input(self) -> str:
        data = self.input_buffer
        if data == "":
            raise RuntimeError(
                "Input buffer is empty, did you call request_input before calling receive_input?"
            )
        # reset buffer
        self.input_buffer = ""
        return data

    @staticmethod
    def clear_display() -> None:
        "If the game is not in Auto Mode, will clear the display"
        # Screen is not cleared in Auto mode since It's better for testing
        # Auto mode is kinda turning into a debug mode (I might make that an option at some point)
        if BasicTerminalInterface.game_mode == "MANUAL":
            # For Windows
            if os.name == "nt":
                os.system("cls")
            # For macOS and Linux
            else:
                os.system("clear")

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
        options_list = "\n".join(choice_list) + "\n"
        chosen_action = ""
        dumb_check = 0
        while chosen_action not in choice_list:
            chosen_action = self.sanitize(input("").upper())
            if chosen_action not in choice_list:
                self.show_ouput(
                    OutputMessage(
                        f"That is not a Valid Option. Try again, valid options are \n{options_list}"
                    )
                )
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
        self.show_ouput(OutputMessage("\n".join(input_messages)))
        return self.sanitize(input()[:max_length])

    def prompt_user(
        self,
        options: list[str],
        prompts: list[str],
    ) -> str:
        ensure_type(options, list, "options")
        ensure_type(prompts, list, "base_messages")

        formatted_message = ""
        for message in prompts:
            formatted_message += f"{message}\n"
        formatted_message += "\n"

        for option in options:
            formatted_message += f"{option}\n"

        formatted_message += "\n"

        self.show_ouput(OutputMessage(formatted_message))

        response = self.validate_input(options)
        return response


trash = """
#### logic that is interface data that has been expunged from the program itself

    ## from New game
    match BasicTerminalInterface.game_mode:
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
from RPyG.utilities import ensure_type


# Function Guidelines
# Functions should return either a string or an int, the upstream functions will handle logic based on the items passed
# Adding the str to bool logic here just adds bloat and over-complicates very, very simple functions


class LEGACYInteraction:
    @staticmethod
    def choose_combat_target(target_party_instance: CombatantParty) -> int:
        ensure_type(target_party_instance, CombatantParty, "target_party_instance")
        target_options: list[str]
        target_options = []

        match BasicTerminalInterface.game_mode:
            case "AUTO":
                # need to move this up stream later and/or merge interaction inside playable actor pepeW
                return target_party_instance.members[0].select_combat_target(
                    target_party_instance
                )

    @staticmethod
    def encounter_enemy() -> str:
        match BasicTerminalInterface.game_mode:
            case "AUTO":
                chosen_action = random.choice(["FLEE", "ATTACK"])
                return chosen_action
            case "MANUAL":

                return prompt_user(encounter_options, encounter_message)
            case _:
                return "ATTACK"

    @staticmethod
    def post_battle(player_party_instance: PlayerParty) -> str:
        ensure_type(player_party_instance, PlayerParty, "player_party_instance")

        match BasicTerminalInterface.game_mode:
            case "AUTO":
                for player_instance in player_party_instance.members:
                    if (
                        player_instance.health < 20
                        and player_instance.inventory.potions != 0
                    ):
                        return "HEAL"
                return "TRAVEL"

            case "MANUAL":

                return prompt_user(post_battle_options, post_battle_message)
            case _:
                return "TRAVEL"

    @staticmethod
    def in_battle(player_instance: PlayableActor) -> str:
        ensure_type(player_instance, PlayableActor, "player_instance")

        match BasicTerminalInterface.game_mode:
            case "AUTO":
                if (
                    player_instance.health <= 40
                    and player_instance.inventory.potions != 0
                ):
                    chosen_action = "HEAL"
                elif player_instance.inventory.potions == 0:
                    display_message(
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
                return 
            case _:
                return "ATTACK"

    @staticmethod
    def at_merchant(player_party_instance: PlayerParty) -> None:
        import math

        ensure_type(player_party_instance, PlayerParty, "player_party_instance")
        display_message("You arrive at a merchant", 1)
        match BasicTerminalInterface.game_mode:
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

                            display_message(
                                f"{player_instance.name} purchases a potion. They now have {player_instance.inventory.potions}",
                                1,
                            )
                        else:
                            display_message(
                                f"{player_instance.name} does not have enough Gold to purchase more potions",
                                1,
                            )
                            break
            case "MANUAL":
                OMG = True

            case _:
                raise ValueError("invalid game mode")

    @staticmethod
    def embark() -> bool:
        match BasicTerminalInterface.game_mode:
            case "AUTO":
                return True
            case "MANUAL":
                embark_options = ["EMBARK", "DRINK"]
                embark_options_message = ["What shall the party do?"]
                player_choice = prompt_user(
                    embark_options, embark_options_message
                )

                while player_choice != "EMBARK":
                    player_choice = prompt_user(
                        embark_options, embark_options_message
                    )

                    match player_choice:
                        case "EMBARK":
                            return True
                        case "DRINK":
                            display_message(
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
        match BasicTerminalInterface.game_mode:
            case "AUTO":
                return True
            case "MANUAL":
                pass
            case _:
                raise ValueError("invalid game mode")

        return True



import textwrap
import time

from RPyG.actors import Combatant, EnemyParty, PlayableActor, PlayerParty

# Only used for Type checking/Hinting
from RPyG.utilities import ensure_type


class LEGACYMessage:
    @staticmethod
    def display_message(message: str, new_line_count: int) -> None:
        Use this function rather than local 'print()' in functions.
        This does basic processing for optimal display and will allow for better output handling when the UI is redone.
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

    # Battle Messages
    @staticmethod
    def battle_hud_message(
        player_party_instance: PlayerParty, enemy_party_instance: EnemyParty
    ) -> None:
        ensure_type(player_party_instance, PlayerParty, "player_party_instance")
        ensure_type(enemy_party_instance, EnemyParty, "enemy_party_instance")



        __class__.display_message(battle_hud_message, 2)

    @staticmethod
    def battle_start_message() -> None:
        battle_start_message = "The Battle Begins!"

        __class__.display_message(battle_start_message, 3)

    @staticmethod
    def empty_travel_message(empty_distance: int) -> None:
        if BasicTerminalInterface.game_mode == "MANUAL":
            time.sleep(2)
        empty_travel_message = f"{'.' * (empty_distance - 1)}"

        __class__.display_message(empty_travel_message, 1)



f"{actor_instance.name} has {actor_instance.health} Health remaining"


"""
