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
        self.kind = kind

        ensure_type(primary_encounter, bool, "primary_encounter")
        self.primary_encounter = primary_encounter

        ensure_type(special_encounter, bool, "special_encounter")
        self.special_encounter = special_encounter

        if next_encounter is not None:
            ensure_type(next_encounter, str, "next_encounter")
        self.next_encounter = next_encounter

        ensure_type(prompts, list, "prompts")
        for prompt in prompts:
            ensure_type(prompt, str, "prompt")
        self.prompts = prompts

        if success_choice is not None:
            ensure_type(success_choice, str, "success_choice")
        self.success_choice = success_choice

        if retry_choice is not None:
            ensure_type(retry_choice, str, "retry_choice")
        self.retry_choice = retry_choice

        if failure_choice is not None:
            ensure_type(failure_choice, str, "failure_choice")
        self.failure_choice = failure_choice

        ensure_type(success_effects, list, "success_effects")
        if success_effects != []:
            for effect in success_effects:
                ensure_type(effect, str, "effect")
        self.success_effects = success_effects

        if retry_effects != []:
            ensure_type(retry_effects, list, "retry_effects")
            for effect in retry_effects:
                ensure_type(effect, str, "effect")
        self.retry_effects = retry_effects

        if failure_effects != []:
            ensure_type(failure_effects, list, "failure_effects")
            for effect in success_effects:
                ensure_type(effect, str, "effect")
        self.failure_effects = failure_effects

        if success_messages != []:
            ensure_type(success_messages, list, "success_messages")
            for effect in success_messages:
                ensure_type(effect, str, "effect")
        self.success_messages = success_messages

        if retry_messages != []:
            ensure_type(retry_messages, list, "retry_messages")
            for effect in retry_messages:
                ensure_type(effect, str, "effect")
        self.retry_messages = retry_messages

        if failure_messages != []:
            ensure_type(failure_messages, list, "failure_messages")
            for effect in failure_messages:
                ensure_type(effect, str, "effect")
        self.failure_messages = failure_messages

    def validate(self) -> bool:
        return True

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
