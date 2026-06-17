import math
import random
from enum import Enum
from typing import TYPE_CHECKING

from RPyG.exceptions import ImpossibleValueException
from RPyG.utilities import ensure_type


if TYPE_CHECKING is True:
    from RPyG.constructs import PlayableActor, PlayerParty


class EffectTarget(Enum):
    ALL = "ALL"
    RANDOM = "RANDOM"


class ActorAction(Enum):
    HEAL = "HEAL"
    DAMAGE = "DAMAGE"
    GAIN_GOLD = "GAIN_GOLD"
    LOSE_GOLD = "LOSE_GOLD"
    GAIN_POTION = "GAIN_POTION"
    LOSE_POTION = "LOSE_POTION"


class SpecialAction(Enum):
    AT_MERCHANT = "AT_MERCHANT"


class EncounterEffect:
    __slots__: tuple[str, ...] = (
        "kind",
        "actor_action",
        "special_action",
        "targets",
        "magnitude",
        "effect_messages",
        "extra_effects",
    )
    kind: str
    actor_action: ActorAction | None
    special_action: SpecialAction | None
    targets: EffectTarget
    magnitude: int
    effect_messages: list[str]
    extra_effects: list[str]

    def __init__(
        self,
        kind: str,
        targets: str,
        magnitude: int,
        effect_messages: list[str],
        extra_effects: list[str],
        actor_action: str | None = None,
        special_action: str | None = None,
    ) -> None:
        ensure_type(kind, str, "kind")

        if actor_action is not None:
            ensure_type(actor_action, str, "actor_action")

        if special_action is not None:
            ensure_type(special_action, str, "special_action")

        ensure_type(targets, str, "targets")
        ensure_type(magnitude, int, "magnitude")
        ensure_type(effect_messages, list, "effect_messages")
        for effect_message in effect_messages:
            ensure_type(effect_message, str, "effect_message")

        ensure_type(extra_effects, list, "extra_effects")
        for effect in extra_effects:
            ensure_type(effect, str, "effect")

        self.kind = kind

        if actor_action is not None:
            self.actor_action = ActorAction(actor_action)
        else:
            self.actor_action = None

        if special_action is not None:
            self.special_action = SpecialAction(special_action)
        else:
            self.special_action = None

        self.targets = EffectTarget(targets)
        self.magnitude = magnitude
        self.effect_messages = effect_messages
        self.extra_effects = extra_effects

    def run_action(self, player_instance: PlayableActor, member_count: int) -> None:
        from RPyG.constructs import PlayableActor

        ensure_type(player_instance, PlayableActor, "player_instance")
        scaled_magnitute = int(self.magnitude / member_count)
        match self.actor_action:
            # only Heal actions do not get scaled by party size
            # it does not make sense that 1 person sleeping in 1 bed heals 3x as much as 3 people in 3 beds
            # random heals are debateble for this concept, but overall this feel fair
            case ActorAction.HEAL:
                player_instance.heal(self.magnitude)
            case ActorAction.DAMAGE:
                player_instance.damage(scaled_magnitute)
            case ActorAction.GAIN_GOLD:
                player_instance.inventory.gain_gold(scaled_magnitute)
            case ActorAction.LOSE_GOLD:
                player_instance.inventory.lose_gold(scaled_magnitute)
            case ActorAction.GAIN_POTION:
                player_instance.inventory.gain_potion(scaled_magnitute)
            case ActorAction.LOSE_POTION:
                player_instance.inventory.lose_potion(scaled_magnitute)
            case None:
                pass
            case _:  # pyright: ignore[reportUnnecessaryComparison]
                raise ImpossibleValueException(f"self.actor_action-{self.actor_action}")  # pyright: ignore[reportUnreachable]

    def process_effect(self) -> None:
        from RPyG.content import ContentLibrary
        from RPyG.core_io import CoreIO, output_models
        from RPyG.game_state import GameState

        # Show any Messages
        game_state = GameState.get_game_state()
        core_io = CoreIO.get_core_io()
        for message in self.effect_messages:
            core_io.send_output(output_models.GenericEncounterMessage(message=message))

        match self.targets:
            case EffectTarget.ALL:
                for member in game_state.player_party.members:
                    self.run_action(
                        member,
                        len(game_state.player_party.members),
                    )
            case EffectTarget.RANDOM:
                self.run_action(
                    random.choice(game_state.player_party.members),
                    len(game_state.player_party.members),
                )
            case _:  # pyright: ignore[reportUnnecessaryComparison]
                raise ImpossibleValueException(f"self.targets - {self.targets}")  # pyright: ignore[reportUnreachable]

        if self.special_action is not None:
            self.process_special_action(game_state.player_party)

        # Run Any Extra Effects
        library = ContentLibrary.get_library()
        for effect_id in self.extra_effects:
            effect = library.encounter_effects[effect_id]
            effect.process_effect()

    def process_special_action(self, player_party_instance: PlayerParty) -> None:
        from RPyG.constructs import PlayerParty

        ensure_type(player_party_instance, PlayerParty, "player_party_instance")
        match self.special_action:
            case None:
                pass
            case SpecialAction.AT_MERCHANT:
                self.visit_merchant(player_party_instance)

    def visit_merchant(
        self,
        player_party_instance: PlayerParty,  # merchant_inventory: None = None
    ) -> None:
        from RPyG.core_io import CoreIO, input_models, output_models

        core_io = CoreIO.get_core_io()
        for player_instance in player_party_instance.members:
            player_choice = ""
            while player_choice != "LEAVE":
                core_io.send_output(
                    output_models.MerchantMenuHudDataMessage(
                        actor_name=player_instance.name,
                        potion_count=player_instance.inventory.potions,
                        gold_count=player_instance.inventory.gold,
                    )
                )
                core_io.request_str_input(
                    input_models.UserPromptRequest(
                        options=[
                            "BUY",
                            "LEAVE",
                            "BUY MAX",
                        ],
                        prompts=[
                            f"{player_instance.name}",
                            f"Gold: {player_instance.inventory.gold}",
                            f"Potions: {player_instance.inventory.potions}",
                            "",
                            "Choose an Action:",
                        ],
                    )
                )
                player_choice = core_io.receive_str_input()
                match player_choice:
                    case "BUY":
                        potion_cost = 25
                        can_buy = player_instance.inventory.spend_gold(potion_cost)
                        if can_buy is True:
                            player_instance.inventory.gain_potion(1)
                            core_io.send_output(
                                output_models.MerchantInteractionMessage(
                                    event=output_models.MerchantInteractionMessage.MerchantEvent(
                                        gold_change=potion_cost,
                                        success=can_buy,
                                        item_name="potion",
                                        item_count_change=1,
                                        buyer_actor_name=player_instance.name,
                                        remaining_gold=player_instance.inventory.gold,
                                        remaining_potions=player_instance.inventory.potions,
                                    )
                                )
                            )
                        else:
                            core_io.send_output(
                                output_models.MerchantInteractionMessage(
                                    event=output_models.MerchantInteractionMessage.MerchantEvent(
                                        gold_change=potion_cost,
                                        success=can_buy,
                                        item_name="potion",
                                        item_count_change=0,
                                        buyer_actor_name=player_instance.name,
                                        remaining_gold=player_instance.inventory.gold,
                                        remaining_potions=player_instance.inventory.potions,
                                    )
                                )
                            )
                            player_choice = "LEAVE"
                    case "BUY MAX":
                        # Using floor to make sure you can't buy 10 potions with 245 gold
                        rounds = math.floor(player_instance.inventory.gold / 25)
                        total_cost = rounds * 25
                        player_instance.inventory.spend_gold(total_cost)  # pyright: ignore[reportUnusedCallResult]
                        player_instance.inventory.gain_potion(rounds)
                        core_io.send_output(
                            output_models.MerchantInteractionMessage(
                                event=output_models.MerchantInteractionMessage.MerchantEvent(
                                    gold_change=total_cost,
                                    success=True,
                                    item_name="potion",
                                    item_count_change=rounds,
                                    buyer_actor_name=player_instance.name,
                                    remaining_gold=player_instance.inventory.gold,
                                    remaining_potions=player_instance.inventory.potions,
                                )
                            )
                        )

                        player_choice = "LEAVE"
                    case _:
                        player_choice = "LEAVE"

    def validate(self) -> bool:
        ensure_type(self.kind, str, "self.kind")
        if self.actor_action is not None:
            ensure_type(self.actor_action, ActorAction, "self.actor_action")
        if self.special_action is not None:
            ensure_type(self.special_action, SpecialAction, "self.special_action")
        ensure_type(self.targets, EffectTarget, "self.targets")
        ensure_type(self.magnitude, int, "self.magnitude")
        ensure_type(self.effect_messages, list, "self.effect_messages")
        for message in self.effect_messages:
            ensure_type(message, str, "self.effect_messages item")
        ensure_type(self.extra_effects, list, "self.extra_effects")
        for effect in self.extra_effects:
            ensure_type(effect, str, "self.extra_effects item")
        return True
