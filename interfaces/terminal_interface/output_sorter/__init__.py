from RPyG.core_io import output_models

from .batle_update_sorter import output_battle_update
from .hud_builder import output_hud_data


def output_message(output: output_models.OutputMessage) -> str:
    match output:
        case output_models.BattleUpdateMessage():
            return output_battle_update(output.event)

        case output_models.BattleHudData():
            return output_hud_data(output)
        case output_models.HealthUpdateMessage():
            message = f"{output.actor_name} has {output.remaining_health}"
            return message
        case _:
            if output.message != "":
                return output.message
            return str(output)
