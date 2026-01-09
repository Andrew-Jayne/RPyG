from typing import TYPE_CHECKING

from RPyG.exceptions import ImpossibleValueException
from RPyG.utilities import ensure_type


if TYPE_CHECKING is True:
    from RPyG.actors import PlayerParty


class Encounter:
    __slots__: tuple[str, ...] = (
        "kind",
        "primary_encounter",
        "special_encounter",
        "next_encounter",
        "prompts",
        "success_choice",
        "retry_choice",
        "failure_choice",
        "success_effects",
        "retry_effects",
        "failure_effects",
        "success_messages",
        "retry_messages",
        "failure_messages",
    )

    kind: str
    primary_encounter: bool
    special_encounter: bool
    next_encounter: str | None
    prompts: list[str]
    success_choice: str | None
    retry_choice: str | None
    failure_choice: str | None
    success_effects: list[str]
    retry_effects: list[str]
    failure_effects: list[str]
    success_messages: list[str]
    retry_messages: list[str]
    failure_messages: list[str]

    def __init__(
        self,
        kind: str,
        primary_encounter: bool,
        special_encounter: bool,
        prompts: list[str],
        success_effects: list[str],
        retry_effects: list[str],
        failure_effects: list[str],
        success_messages: list[str],
        retry_messages: list[str],
        failure_messages: list[str],
        next_encounter: str | None = None,
        success_choice: str | None = None,
        retry_choice: str | None = None,
        failure_choice: str | None = None,
    ) -> None:
        ensure_type(kind, str, "kind")
        ensure_type(primary_encounter, bool, "primary_encounter")
        ensure_type(special_encounter, bool, "special_encounter")

        if next_encounter is not None:
            ensure_type(next_encounter, str, "next_encounter")

        ensure_type(prompts, list, "prompts")
        for prompt in prompts:
            ensure_type(prompt, str, "prompt")

        if success_choice is not None:
            ensure_type(success_choice, str, "success_choice")

        if retry_choice is not None:
            ensure_type(retry_choice, str, "retry_choice")

        if failure_choice is not None:
            ensure_type(failure_choice, str, "failure_choice")

        ensure_type(success_effects, list, "success_effects")
        for effect in success_effects:
            ensure_type(effect, str, "effect")

        ensure_type(retry_effects, list, "retry_effects")
        for effect in retry_effects:
            ensure_type(effect, str, "effect")

        ensure_type(failure_effects, list, "failure_effects")
        for effect in failure_effects:
            ensure_type(effect, str, "effect")

        ensure_type(success_messages, list, "success_messages")
        for message in success_messages:
            ensure_type(message, str, "message")

        ensure_type(retry_messages, list, "retry_messages")
        for message in retry_messages:
            ensure_type(message, str, "message")

        ensure_type(failure_messages, list, "failure_messages")
        for message in failure_messages:
            ensure_type(message, str, "message")

        self.kind = kind
        self.primary_encounter = primary_encounter
        self.special_encounter = special_encounter
        self.next_encounter = next_encounter
        self.prompts = prompts
        self.success_choice = success_choice
        self.retry_choice = retry_choice
        self.failure_choice = failure_choice
        self.success_effects = success_effects
        self.retry_effects = retry_effects
        self.failure_effects = failure_effects
        self.success_messages = success_messages
        self.retry_messages = retry_messages
        self.failure_messages = failure_messages

    def process_encounter(self, player_party_instance: PlayerParty) -> None:
        from RPyG.content import ContentLibrary
        from RPyG.core_io import CoreIO
        from RPyG.core_io.io_models import OutputMessage, UserPromptRequest

        core_io = CoreIO.get_core_io()
        library = ContentLibrary.get_library()

        # Process choices
        choice_options: list[str | None] = []
        choice_options.append(self.success_choice)
        choice_options.append(self.retry_choice)
        choice_options.append(self.failure_choice)
        if choice_options != [None, None, None]:
            core_io.request_input(
                UserPromptRequest(
                    options=choice_options,
                    prompts=self.prompts,
                )
            )
            user_choice = core_io.receive_input()
            while user_choice == self.retry_choice:
                core_io.request_input(
                    UserPromptRequest(
                        prompts=self.retry_messages,
                        options=choice_options,
                    )
                )
                for effect_id in self.retry_effects:
                    effect = library.encounter_effects[effect_id]
                    effect.process_effect(player_party_instance)
                user_choice = core_io.receive_input()
            match user_choice:
                case self.success_choice:
                    for message in self.success_messages:
                        core_io.send_output(OutputMessage(message))
                    for effect_id in self.success_effects:
                        effect = library.encounter_effects[effect_id]
                        effect.process_effect(player_party_instance)

                case self.failure_choice:
                    for message in self.failure_messages:
                        core_io.send_output(OutputMessage(message))
                    for effect_id in self.failure_effects:
                        effect = library.encounter_effects[effect_id]
                        effect.process_effect(player_party_instance)

                case _:
                    raise ImpossibleValueException("user_choice")

    def validate(self) -> bool:
        ensure_type(self.kind, str, "self.kind")
        ensure_type(self.primary_encounter, bool, "self.primary_encounter")
        ensure_type(self.special_encounter, bool, "self.special_encounter")
        if self.next_encounter is not None:
            ensure_type(self.next_encounter, str, "self.next_encounter")
        ensure_type(self.prompts, list, "self.prompts")
        for prompt in self.prompts:
            ensure_type(prompt, str, "self.prompts item")
        if self.success_choice is not None:
            ensure_type(self.success_choice, str, "self.success_choice")
        if self.retry_choice is not None:
            ensure_type(self.retry_choice, str, "self.retry_choice")
        if self.failure_choice is not None:
            ensure_type(self.failure_choice, str, "self.failure_choice")
        ensure_type(self.success_effects, list, "self.success_effects")
        for effect in self.success_effects:
            ensure_type(effect, str, "self.success_effects item")
        ensure_type(self.retry_effects, list, "self.retry_effects")
        for effect in self.retry_effects:
            ensure_type(effect, str, "self.retry_effects item")
        ensure_type(self.failure_effects, list, "self.failure_effects")
        for effect in self.failure_effects:
            ensure_type(effect, str, "self.failure_effects item")
        ensure_type(self.success_messages, list, "self.success_messages")
        for message in self.success_messages:
            ensure_type(message, str, "self.success_messages item")
        ensure_type(self.retry_messages, list, "self.retry_messages")
        for message in self.retry_messages:
            ensure_type(message, str, "self.retry_messages item")
        ensure_type(self.failure_messages, list, "self.failure_messages")
        for message in self.failure_messages:
            ensure_type(message, str, "self.failure_messages item")
        return True
