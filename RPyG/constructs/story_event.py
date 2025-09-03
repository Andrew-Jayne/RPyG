from dataclasses import dataclass

from RPyG.utilites import ensure_type


# Fully Runtime Immutable
@dataclass(frozen=True, slots=True)
class StoryEvent:
    messages: tuple[str, ...]
    success_messages: tuple[str, ...]
    failure_messages: tuple[str, ...]

    def __post_init__(self) -> None:
        ensure_type(self.messages, list, "messages")
        ensure_type(self.success_messages, list, "success_messages")
        ensure_type(self.failure_messages, list, "failure_messages")

        if len(self.messages) > 0:
            for messages_item in self.messages:
                ensure_type(messages_item, str, "messages_item")
        if len(self.messages) > 0:
            for success_messages_item in self.success_messages:
                ensure_type(success_messages_item, str, "success_messages_item")
        if len(self.failure_messages) > 0:
            for failure_messages_item in self.failure_messages:
                ensure_type(failure_messages_item, str, "failure_messages_item")
