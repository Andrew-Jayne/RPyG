from typing import Any

from RPyG.utilites import ensure_type


class StoryEvent:
    messages: list[str]
    success_messages: list[str]
    failure_messages: list[str]

    def __init__(
        self,
        messages: list[str],
        success_messages: list[str],
        failure_messages: list[str],
    ) -> None:
        ensure_type(messages, list, "messages")
        ensure_type(success_messages, list, "success_messages")
        ensure_type(failure_messages, list, "failure_messages")

        if len(messages) > 0:
            for messages_item in messages:
                ensure_type(messages_item, str, "messages_item")
        if len(messages) > 0:
            for success_messages_item in success_messages:
                ensure_type(success_messages_item, str, "success_messages_item")
        if len(failure_messages) > 0:
            for failure_messages_item in failure_messages:
                ensure_type(failure_messages_item, str, "failure_messages_item")

        self.messages = messages
        self.success_messages = success_messages
        self.failure_messages = failure_messages


class StoryLibrary:
    story_events: dict[int, StoryEvent]

    def __init__(self, event_data: dict[str, Any]) -> None:
        ensure_type(event_data, dict, "event_data")

        story_events: dict[int, StoryEvent] = {}

        for event_data_key, event_data_value in event_data.items():
            ensure_type(event_data_key, str, "event_data_key")
            ensure_type(event_data_value, dict, "event_data_value")

            story_events[int(event_data_key)] = StoryEvent(**event_data_value)

        self.story_events = story_events
