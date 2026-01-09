import os
import textwrap
import time
from typing import Literal, cast, override

from RPyG import (
    CustomTextRequest,
    InputRequest,
    OutputMessage,
    RPyGInterface,
    UserPromptRequest,
)
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
        self.show_ouput(OutputMessage(welcome_message, line_delay=0))

    @override
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
        # Sleep before print based on line delay
        if output.reset_display is True:
            self.clear_display()
        time.sleep(output.line_delay)
        print(wrapped_message.rstrip("\n"), end=ending)

    @override
    def request_input(self, request: InputRequest) -> None:
        ensure_type(request, InputRequest, "request")
        match type(request).__name__:
            case "InputRequest":
                raise NotImplementedError
            case "UserPromptRequest":
                prompt_request = cast(UserPromptRequest, request)
                displayable_options: list[str] = []
                for item in prompt_request.options:
                    if item is not None:
                        displayable_options.append(item)
                content = self.prompt_user(
                    options=displayable_options,
                    prompts=prompt_request.prompts,
                    show_options=prompt_request.show_options,
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

    @override
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
        # For Windows
        if os.name == "nt":
            os.system("cls")  # pyright: ignore[reportUnusedCallResult]
        # For macOS and Linux
        else:
            os.system('clear && printf "\\e[3J"')  # pyright: ignore[reportUnusedCallResult]

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
        self, options: list[str], prompts: list[str], show_options: bool = True
    ) -> str:
        ensure_type(options, list, "options")
        ensure_type(prompts, list, "base_messages")

        formatted_message = ""
        for message in prompts:
            formatted_message += f"{message}\n"
        formatted_message += "\n"

        if show_options is True:
            for option in options:
                formatted_message += f"{option}\n"

        formatted_message += "\n"

        self.show_ouput(OutputMessage(formatted_message))

        response = self.validate_input(options)
        return response
