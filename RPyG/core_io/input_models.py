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
    # Barf this needs to be better
    options: list[str] | list[str | None]
    prompts: list[str]
    show_options: bool = True


@dataclass
class CustomTextRequest(InputRequest):
    prompts: list[str]
    max_length: int
