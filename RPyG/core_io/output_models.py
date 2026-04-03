from dataclasses import dataclass

from RPyG.utilities import ensure_type


@dataclass
class OutputMessage:
    message: str

    def __post_init__(self) -> None:
        ensure_type(self.message, str, "output_message")


@dataclass(kw_only=True)
class EmptyDistanceMessage(OutputMessage):
    distance: int
    message: str = ""

    def __post_init__(self) -> None:
        ensure_type(self.distance, int, "distance")
        ensure_type(self.message, str, "message")
