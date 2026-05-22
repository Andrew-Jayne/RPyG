from RPyG.core_io import output_models

from .. import text_strings


def output_battle_update(event: output_models.BattleUpdateMessage.BattleEvent) -> str:
    match event:
        case output_models.BattleUpdateMessage.AttackEvent():
            attack_message = text_strings.attack_string.format(
                source_actor_name=event.source_actor_name,
                attack_name=event.attack_name,
                magnitude=event.magnitude,
                target_actor_name=event.target_actor_name,
            )
            if event.is_critical is True:
                attack_message = (
                    attack_message
                    + "\n"
                    + text_strings.critical_attack_string.format(
                        source_actor_name=event.source_actor_name
                    )
                )

            return attack_message
        case output_models.BattleUpdateMessage.AoeAttackEvent():
            aoe_message = text_strings.aoe_attack_string.format(
                source_actor_name=event.source_actor_name,
                attack_message=event.attack_name,
                per_target_damage=event.per_target_damage,
            )
            if event.is_critical is True:
                aoe_message = (
                    aoe_message
                    + "\n"
                    + text_strings.aoe_critical_string.format(
                        source_actor_name=event.source_actor_name
                    )
                )

            if event.self_damage is True:
                aoe_message = aoe_message + text_strings.aoe_self_damage_string.format(
                    source_actor_name=event.source_actor_name,
                    attack_name=event.attack_name,
                    self_damage_magnitude=event.self_damage_magnitude,
                )

            return aoe_message

        case output_models.BattleUpdateMessage.DoubleAttackEvent():
            if event.self_damage is True:
                return text_strings.self_damage_str.format(
                    source_actor_name=event.source_actor_name,
                    secondary_target_name=event.secondary_target_name,
                    self_damage_magnitude=event.self_damage_magnitude,
                )
            return ""

        case output_models.BattleUpdateMessage.DismemberAttackEvent():
            if event.valid_target is False:
                return text_strings.no_valid_targets_strings
            if event.target_decapitated is True:
                return text_strings.decapitate_string.format(
                    source_actor_name=event.source_actor_name,
                    target_actor_name=event.target_actor_name,
                )

            return text_strings.dismember_string.format(
                source_actor_name=event.source_actor_name,
                target_actor_name=event.target_actor_name,
            )

        # case output_models.BattleUpdateMessage.BattleEvent():
        #     return event.message
        case _:
            return str(event)
