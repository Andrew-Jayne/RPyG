from enum import Enum

from RPyG.actors import EnemyParty, PlayerParty
from RPyG.combat import battle
from RPyG.constructs import Dungeon
from RPyG.core_io import CoreIO
from RPyG.core_io.io_models import OutputMessage
from RPyG.exceptions import ImpossibleValueException
from RPyG.game_state import save_game
from RPyG.utilities import ensure_type


class StoryEventType(Enum):
    BOSS_ENCOUNTER = "BOSS_ENCOUNTER"
    DUNGEON_ENCOUNTER = "DUNGEON_ENCOUNTER"
    ENCOUNTER = "ENCOUNTER"


class StoryEvent:
    __slots__: tuple[str, ...] = (
        "kind",
        "event_type",
        "progress_trigger",
        "messages",
        "success_messages",
        "failure_messages",
        "enemy_id",
        "dungeon_id",
        "encounter_id",
    )
    kind: str
    event_type: StoryEventType
    progress_trigger: int
    messages: tuple[str, ...]
    success_messages: tuple[str, ...]
    failure_messages: tuple[str, ...]
    enemy_id: str | None
    dungeon_id: str | None
    encounter_id: str | None

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
        encounter_id: str | None = None,
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

        if encounter_id is not None:
            ensure_type(encounter_id, str, "encounter_id")

        # Set attributes
        self.kind = kind
        self.event_type = StoryEventType(event_type)
        self.progress_trigger = progress_trigger
        self.messages = tuple(messages)
        self.success_messages = tuple(success_messages)
        self.failure_messages = tuple(failure_messages)
        self.enemy_id = enemy_id
        self.dungeon_id = dungeon_id
        self.encounter_id = encounter_id

    def validate(self) -> bool:
        return True

    def trigger(self, player_party_instance: PlayerParty) -> None:
        ensure_type(player_party_instance, PlayerParty, "player_party_instance")
        from RPyG.content import ContentLibrary

        content_library = ContentLibrary.get_library()
        core_io = CoreIO.get_core_io()
        match self.event_type:
            case StoryEventType.BOSS_ENCOUNTER:
                if self.enemy_id is None:
                    raise ValueError(
                        "enemy_id must be specified for BOSS_ENCOUNTER events"
                    )

                enemy_instance = content_library.enemies[self.enemy_id]

                for message in self.messages:
                    core_io.send_output(
                        OutputMessage(
                            message.format(party_name=player_party_instance.name)
                        )
                    )

                enemy_party = EnemyParty(enemy_instance.name, [enemy_instance])
                battle(player_party_instance, enemy_party)
                if len(player_party_instance.members) != 0:
                    for message in self.success_messages:
                        core_io.send_output(
                            OutputMessage(
                                message.format(party_name=player_party_instance.name)
                            )
                        )
                    save_game(player_party_instance)
                else:
                    for message in self.failure_messages:
                        core_io.send_output(
                            OutputMessage(
                                message.format(party_name=player_party_instance.name)
                            )
                        )
            case StoryEventType.DUNGEON_ENCOUNTER:
                ## still a little sloppy
                if self.dungeon_id is None:
                    raise ValueError(
                        "dungeon_id must be specified for DUNGEON_ENCOUNTER events"
                    )
                for message in self.messages:
                    core_io.send_output(
                        OutputMessage(
                            message.format(party_name=player_party_instance.name)
                        )
                    )

                if self.dungeon_id not in content_library.dungeons.keys():
                    raise FileNotFoundError(
                        f"Unable to locate Dungeon with the ID {self.dungeon_id}, avalible IDs are {content_library.dungeons.keys()}"
                    )
                active_dungeon: Dungeon = content_library.dungeons[self.dungeon_id]
                active_dungeon.traverse_dungeon(player_party_instance)
                if len(player_party_instance.members) != 0:
                    for message in self.success_messages:
                        core_io.send_output(
                            OutputMessage(
                                message.format(party_name=player_party_instance.name)
                            )
                        )
                    save_game(player_party_instance)
                else:
                    for message in self.failure_messages:
                        core_io.send_output(
                            OutputMessage(
                                message.format(party_name=player_party_instance.name)
                            )
                        )
            case StoryEventType.ENCOUNTER:
                for message in self.messages:
                    core_io.send_output(
                        OutputMessage(
                            message.format(party_name=player_party_instance.name)
                        )
                    )
                if self.encounter_id is not None:
                    if self.encounter_id not in content_library.encounters.keys():
                        raise FileNotFoundError(
                            f"Unable to locate encounter with the ID {self.encounter_id}, avalible IDs are {content_library.encounters.keys()}"
                        )
                    encounter = content_library.encounters[self.encounter_id]
                    encounter.process_encounter(player_party_instance)
                if len(player_party_instance.members) != 0:
                    for message in self.success_messages:
                        core_io.send_output(
                            OutputMessage(
                                message.format(party_name=player_party_instance.name)
                            )
                        )
                else:
                    for message in self.failure_messages:
                        core_io.send_output(
                            OutputMessage(
                                message.format(party_name=player_party_instance.name)
                            )
                        )
            case _:  # pyright: ignore[reportUnnecessaryComparison]
                raise ImpossibleValueException(f"self.event_type: {self.event_type}")  # pyright: ignore[reportUnreachable]
