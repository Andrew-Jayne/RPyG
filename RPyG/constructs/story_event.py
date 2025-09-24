from enum import Enum

from RPyG.actors import EnemyParty, PlayerParty
from RPyG.combat import battle
from RPyG.constructs import Dungeon
from RPyG.content import ContentLibrary
from RPyG.core_io import CoreIO
from RPyG.core_io.io_models import OutputMessage
from RPyG.gameState.file import save_game
from RPyG.utilites import ensure_type


class StoryEventType(Enum):
    BOSS_ENCOUNTER = "BOSS_ENCOUNTER"
    DUNGEON_ENCOUNTER = "DUNGEON_ENCOUNTER"
    ONE_CHOICE_EVENT = "ONE_CHOICE_EVENT"
    MULTI_CHOICE_EVENT = "MULTI_CHOICE_EVENT"


class StoryEvent:
    __slots__ = (
        "kind",
        "event_type",
        "progress_trigger",
        "messages",
        "success_messages",
        "failure_messages",
        "enemy_id",
        "dungeon_id",
    )
    kind: str
    event_type: StoryEventType
    progress_trigger: int
    messages: tuple[str, ...]
    success_messages: tuple[str, ...]
    failure_messages: tuple[str, ...]
    enemy_id: str | None
    dungeon_id: str | None

    def __init__(
        self,
        kind: str,
        event_type: str,
        progress_trigger: int,
        messages: list[str],
        success_messages: list[str],
        failure_messages: list[str],
        enemy_id: str | None = None,
        dungeon_id: str | None = None,
    ) -> None:
        # Validate types
        ensure_type(kind, str, "kind")
        ensure_type(event_type, str, "event_type")
        ensure_type(progress_trigger, int, "progress_trigger")
        ensure_type(messages, list, "messages")
        ensure_type(success_messages, list, "success_messages")
        ensure_type(failure_messages, list, "failure_messages")

        # Validate message items
        for messages_item in messages:
            ensure_type(messages_item, str, "messages_item")
        for success_messages_item in success_messages:
            ensure_type(success_messages_item, str, "success_messages_item")
        for failure_messages_item in failure_messages:
            ensure_type(failure_messages_item, str, "failure_messages_item")

        if enemy_id is not None:
            ensure_type(enemy_id, str, "enemy_id")

        if dungeon_id is not None:
            ensure_type(dungeon_id, str, "dungeon_id")

        # Set attributes
        self.kind = kind
        self.event_type = StoryEventType(event_type)
        self.progress_trigger = progress_trigger
        self.messages = tuple(messages)
        self.success_messages = tuple(success_messages)
        self.failure_messages = tuple(failure_messages)
        self.enemy_id = enemy_id
        self.dungeon_id = dungeon_id

    @staticmethod
    def send_special_encounter_message(
        progress_value,
        party_name,
        message_type,
    ) -> None:
        core_io = CoreIO.get_core_io()
        content_library = ContentLibrary.get_library()

        all_events = content_library.story_events

        current_event = all_events[progress_value]
        match message_type:
            case "messages":
                active_messages = current_event.messages
            case "success_messages":
                active_messages = current_event.success_messages
            case "failure_messages":
                active_messages = current_event.failure_messages
            case _:
                raise ValueError(
                    'Message type must be one of ["messages", "success_messages", "failure_messages"]'
                )
        for message in active_messages:
            core_io.send_output(OutputMessage(message.format(party_name=party_name)))

    def validate(self) -> bool:
        return True

    def trigger(self, player_party_instance: PlayerParty) -> None:
        ensure_type(player_party_instance, PlayerParty, "player_party_instance")
        content_library = ContentLibrary.get_library()
        match self.event_type:
            case StoryEventType.BOSS_ENCOUNTER:
                if self.enemy_id is None:
                    raise ValueError(
                        "enemy_id must be specified for BOSS_ENCOUNTER events"
                    )

                enemy_instance = content_library.enemies[self.enemy_id]

                self.send_special_encounter_message(
                    player_party_instance.progress,
                    player_party_instance.name,
                    "messages",
                )

                enemy_party = EnemyParty(enemy_instance.name, [enemy_instance])
                battle(player_party_instance, enemy_party)
                if len(player_party_instance.members) != 0:
                    self.send_special_encounter_message(
                        player_party_instance.progress,
                        player_party_instance.name,
                        "success_messages",
                    )
                    save_game(player_party_instance)
                else:
                    self.send_special_encounter_message(
                        player_party_instance.progress,
                        player_party_instance.name,
                        "failure_messages",
                    )
            case StoryEventType.DUNGEON_ENCOUNTER:
                ## still a little sloppy
                if self.dungeon_id is None:
                    raise ValueError(
                        "dungeon_id must be specified for DUNGEON_ENCOUNTER events"
                    )
                self.send_special_encounter_message(
                    player_party_instance.progress,
                    player_party_instance.name,
                    "messages",
                )

                if self.dungeon_id not in content_library.dungeons.keys():
                    raise FileNotFoundError(
                        f"Unable to locate Dungeon with the ID {self.dungeon_id}, avalible IDs are {content_library.dungeons.keys()}"
                    )
                active_dungeon: Dungeon = content_library.dungeons[self.dungeon_id]
                active_dungeon.travese_dungeon(player_party_instance)
                save_game(player_party_instance)
            case StoryEventType.ONE_CHOICE_EVENT:
                ## needs <- this is A LOT of stuff just for 1 half of the events
                # options list[str]
                # success_choice str
                # prompt str
                # retry_message str
                # success_message str
                # end_actor_actions list(ActionKey: str, Magnitide: int) <- this feels jank
                pass
            case StoryEventType.MULTI_CHOICE_EVENT:
                raise NotImplementedError
            case _:
                raise ValueError(f"Invalid StoryEvent Type: {self.event_type}")
