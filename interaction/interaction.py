import random

import config

# Only Used For Type Hinting/Checking
from actors import PlayableActor, PlayerParty, EnemyParty
from message.message import Message
from utilites.utilities import ensure_type


# Interaction Function Guidelines
# Functions should return either a string or an int, the upstream functions will handle logic based on the items passed
# Adding the str to bool logic here just adds bloat and over-complicates very, very simple functions


class Interaction:
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

    @staticmethod
    def validate_input(choice_list: list[str]) -> str:
        """
        Checks that the string input by the user is in the allowed list of responses
        Sanitizes the input then returns up to the max length specified
        """
        options_list = "\n".join(choice_list)
        chosen_action = ""
        dumb_check = 0
        while chosen_action not in choice_list:
            chosen_action = Interaction.sanitize(input("").upper())
            if chosen_action not in choice_list:
                Message.display_message(
                    "That is not a Valid Option. Try again, valid options are", 2
                )
                Message.display_message(options_list, 1)
                dumb_check += 1
                if dumb_check == 10:
                    raise FileNotFoundError(
                        "Look it's not hard, just enter a valid choice...."
                    )
        return chosen_action

    @staticmethod
    def custom_text_entry(input_messages: list[str], max_length: int) -> str:
        for message in input_messages:
            Message.display_message(message, 1)
        return Interaction.sanitize(input()[:max_length])

    @staticmethod
    def prompt_user(
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

        Message.display_message(formatted_message, 1)

        if return_index is True:
            int_options: list[str]
            int_options = []
            for i in range(len(options) + 1):
                int_options.append(str(i))
            options = int_options

        response = Interaction.validate_input(options)
        return response

    @staticmethod
    def choose_combat_target(target_party_instance: EnemyParty) -> int:
        ensure_type(target_party_instance, EnemyParty, "target_party_instance")
        target_options: list[str]
        target_options = []
        match config.GLOBAL_GAME_MODE:
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
        match config.GLOBAL_GAME_MODE:
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

        match config.GLOBAL_GAME_MODE:
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

        match config.GLOBAL_GAME_MODE:
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

        Message.display_message("You arrive at a merchant", 1)
        match config.GLOBAL_GAME_MODE:
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
        match config.GLOBAL_GAME_MODE:
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
        match config.GLOBAL_GAME_MODE:
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
        match config.GLOBAL_GAME_MODE:
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
        match config.GLOBAL_GAME_MODE:
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
        match config.GLOBAL_GAME_MODE:
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
