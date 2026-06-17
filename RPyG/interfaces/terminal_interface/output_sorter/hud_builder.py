from RPyG.core_io.output_models import BattleHudData


def output_hud_data(event_data: BattleHudData) -> str:
    hud_data = ""
    for player_stats in event_data.player_party_data.member_stats:
        if player_stats.alive is True:
            hud_data += f"{player_stats.name}: {player_stats.health}\n"
    hud_data += "\n"
    for enemy_stats in event_data.enemy_party_data.member_stats:
        if enemy_stats.alive is True:
            hud_data += f"{enemy_stats.name}: {enemy_stats.health}\n"
    return hud_data
