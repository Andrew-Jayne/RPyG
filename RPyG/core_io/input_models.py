from dataclasses import dataclass

from RPyG.utilities import ensure_type


# Input requests
@dataclass
class InputRequest:
    prompts: list[str]

    def __post_init__(self) -> None:
        ensure_type(self.prompts, list, "prompts")
        for prompt in self.prompts:
            ensure_type(prompt, str, "prompt")


@dataclass
class UserPromptRequest(InputRequest):
    options: list[str]
    prompts: list[str]

    def __post_init__(self) -> None:
        InputRequest.__post_init__(self)
        ensure_type(self.options, list, "options")
        for option in self.options:
            ensure_type(option, str, "option")


@dataclass
class CustomTextRequest(InputRequest):
    prompts: list[str]
    max_length: int

    def __post_init__(self) -> None:
        InputRequest.__post_init__(self)
        ensure_type(self.max_length, int, "max_length")
        if self.max_length < 1:
            raise ValueError(
                f"CustomTextRequest.max_length must be a non-zero positive number, got {self.max_length}"
            )
