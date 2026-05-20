from dataclasses import dataclass

from RPyG.utilities import ensure_type


@dataclass(kw_only=True, frozen=True, slots=True)
class OutputMessage:
    message: str

    def __post_init__(self) -> None:
        ensure_type(self.message, str, "output_message")
