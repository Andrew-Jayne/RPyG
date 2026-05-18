from enum import Enum

from RPyG.combat import battle
from RPyG.constructs import EnemyParty
from RPyG.exceptions import ImpossibleValueException
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
    progress_trigger: str
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
        self.progress_trigger = str(progress_trigger)
        self.messages = tuple(messages)
        self.success_messages = tuple(success_messages)
        self.failure_messages = tuple(failure_messages)
        self.enemy_id = enemy_id
        self.dungeon_id = dungeon_id
        self.encounter_id = encounter_id

    def trigger(self) -> None:
        from RPyG.content import ContentLibrary
        from RPyG.core_io import CoreIO, output_models
        from RPyG.game_state import GameState

        content_library = ContentLibrary.get_library()
        core_io = CoreIO.get_core_io()
        game_state = GameState.get_game_state()

        match self.event_type:
            case StoryEventType.BOSS_ENCOUNTER:
                if self.enemy_id is None:
                    raise ValueError(
                        "enemy_id must be specified for BOSS_ENCOUNTER events"
                    )

                enemy_instance = content_library.enemies[self.enemy_id]

                for message in self.messages:
                    core_io.send_output(
                        output_models.OutputMessage(
                            message.format(party_name=game_state.player_party.name)
                        )
                    )

                game_state.set_enemy_party(
                    EnemyParty(
                        enemy_instance.name,
                        [enemy_instance],
                    )
                )
                battle()
                if len(game_state.player_party.members) != 0:
                    for message in self.success_messages:
                        core_io.send_output(
                            output_models.OutputMessage(
                                message.format(party_name=game_state.player_party.name)
                            )
                        )
                    core_io.interface.save_game_state(game_state)
                else:
                    for message in self.failure_messages:
                        core_io.send_output(
                            output_models.OutputMessage(
                                message.format(party_name=game_state.player_party.name)
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
                        output_models.OutputMessage(
                            message.format(party_name=game_state.player_party.name)
                        )
                    )

                if self.dungeon_id not in content_library.dungeons.keys():
                    raise FileNotFoundError(
                        f"Unable to locate Dungeon with the ID {self.dungeon_id}, available IDs are {content_library.dungeons.keys()}"
                    )
                game_state.set_dungeon(content_library.dungeons[self.dungeon_id])
                with game_state.borrow_dungeon() as dungeon:
                    dungeon.traverse_dungeon()
                if len(game_state.player_party.members) != 0:
                    for message in self.success_messages:
                        core_io.send_output(
                            output_models.OutputMessage(
                                message.format(party_name=game_state.player_party.name)
                            )
                        )
                    core_io.interface.save_game_state(game_state)
                else:
                    for message in self.failure_messages:
                        core_io.send_output(
                            output_models.OutputMessage(
                                message.format(party_name=game_state.player_party.name)
                            )
                        )
            case StoryEventType.ENCOUNTER:
                for message in self.messages:
                    core_io.send_output(
                        output_models.OutputMessage(
                            message.format(party_name=game_state.player_party.name)
                        )
                    )
                if self.encounter_id is not None:
                    if self.encounter_id not in content_library.encounters.keys():
                        raise FileNotFoundError(
                            f"Unable to locate encounter with the ID {self.encounter_id}, available IDs are {content_library.encounters.keys()}"
                        )
                    encounter = content_library.encounters[self.encounter_id]
                    encounter.process_encounter()
                if len(game_state.player_party.members) != 0:
                    for message in self.success_messages:
                        core_io.send_output(
                            output_models.OutputMessage(
                                message.format(party_name=game_state.player_party.name)
                            )
                        )
                else:
                    for message in self.failure_messages:
                        core_io.send_output(
                            output_models.OutputMessage(
                                message.format(party_name=game_state.player_party.name)
                            )
                        )
            case _:  # pyright: ignore[reportUnnecessaryComparison]
                raise ImpossibleValueException(f"self.event_type: {self.event_type}")  # pyright: ignore[reportUnreachable]

    def validate(self) -> bool:
        ensure_type(self.kind, str, "self.kind")
        ensure_type(self.event_type, StoryEventType, "self.event_type")
        ensure_type(self.progress_trigger, str, "self.progress_trigger")
        ensure_type(self.messages, tuple, "self.messages")
        ensure_type(self.success_messages, tuple, "self.success_messages")
        ensure_type(self.failure_messages, tuple, "self.failure_messages")
        if self.enemy_id is not None:
            ensure_type(self.enemy_id, str, "self.enemy_id")
        if self.dungeon_id is not None:
            ensure_type(self.dungeon_id, str, "self.dungeon_id")
        if self.encounter_id is not None:
            ensure_type(self.encounter_id, str, "self.encounter_id")

        return True
