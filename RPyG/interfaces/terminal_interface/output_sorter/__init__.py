from RPyG.core_io import output_models

from .. import text_strings
from .batle_update_sorter import output_battle_update
from .hud_builder import output_hud_data


def output_message(output: output_models.OutputMessage) -> str:
    match output:
        case output_models.BattleUpdateMessage():
            return output_battle_update(output.event)

        case output_models.BattleHudData():
            return output_hud_data(output)

        case output_models.HealthUpdateMessage():
            return text_strings.health_remaining_string.format(
                actor_name=output.actor_name,
                remaining_health=output.remaining_health,
            )

        case output_models.UsePotionMessage():
            if output.potions_used > 0:
                return text_strings.drink_potion_string.format(
                    actor_name=output.actor_name
                )
            if output.fully_healed is True:
                return text_strings.already_full_heal_string.format(
                    actor_name=output.actor_name
                )
            return text_strings.no_potions_string.format(actor_name=output.actor_name)

        case output_models.UseGoldMessage():
            if isinstance(output.event, output_models.UseGoldMessage.NoGoldEvent):
                return text_strings.no_gold_string.format(actor_name=output.actor_name)
            if isinstance(
                output.event, output_models.UseGoldMessage.InsufficientGoldEvent
            ):
                return text_strings.insufficient_gold_string.format(
                    actor_name=output.actor_name
                )
            return ""

        case output_models.ActorDefeatedMessage():
            return text_strings.actor_defeated_string.format(
                actor_name=output.actor_name
            )

        case output_models.BattleStartMessage():
            return text_strings.battle_start_string

        case output_models.BattleEndMessage():
            if output.player_victory is True:
                return text_strings.battle_victory_string.format(
                    enemy_party_name=output.enemy_party_name
                )
            return ""

        case output_models.EnemyEncounterMessage():
            return text_strings.enemy_encounter_string.format(
                enemy_party_name=output.enemy_party_name
            )

        case output_models.FleeResultMessage():
            if output.success is True:
                return text_strings.flee_success_string.format(
                    actor_name=output.actor_name,
                    enemy_party_name=output.enemy_party_name,
                )
            return text_strings.flee_fail_string.format(
                actor_name=output.actor_name,
                enemy_party_name=output.enemy_party_name,
            )

        case output_models.MerchantMenuHudDataMessage():
            return text_strings.merchant_menu_string.format(
                actor_name=output.actor_name,
                potion_count=output.potion_count,
                gold_count=output.gold_count,
            )

        case output_models.MerchantInteractionMessage():
            if output.event.success is False:
                return text_strings.merchant_insufficient_string.format(
                    buyer_actor_name=output.event.buyer_actor_name
                )
            return text_strings.merchant_buy_string.format(
                buyer_actor_name=output.event.buyer_actor_name,
                remaining_potions=output.event.remaining_potions,
                remaining_gold=output.event.remaining_gold,
            )

        case output_models.EmptyDistanceMessage():
            return "*" * output.distance

        case output_models.EventAfterEmptyMessage():
            return text_strings.travel_distance_string.format(distance=output.distance)

        case output_models.DungeonUpdateMessage():
            return output.event.message

        case output_models.GameEndMessage():
            return output.post_game_recap

        case _:
            if output.message != "":
                return output.message
            return str(output)
