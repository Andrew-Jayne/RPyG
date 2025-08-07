from RPyG.content import ContentPaths
from RPyG.core_io import RPyGInterface


def launch_game(
    content_paths: ContentPaths,
    interface: RPyGInterface,
) -> None:
    from RPyG.content import ContentLibrary
    from RPyG.core_io import CoreIO
    from RPyG.encounters.encounter import check_for_encounter
    from RPyG.gameState.game_start import start_game

    # These are gateway singletons so we just need to create them
    # at a scope where they live for the lifetime of the applications
    ContentLibrary(content_paths)
    CoreIO(interface)

    player_party_instance = start_game()

    rounds_without_encounter = 0
    # The Key Loop
    core_io = CoreIO.get_core_io()
    while player_party_instance.progress != 100:
        player_party_instance.progress += 1
        match check_for_encounter(player_party_instance, rounds_without_encounter):
            case True:
                rounds_without_encounter = 1
            case False:
                rounds_without_encounter += 1
                core_io.send_output(
                    {"message": f"no_events {rounds_without_encounter}"}
                )

        if len(player_party_instance.members) == 0:
            break

    if player_party_instance.members == []:
        # [] means all players are in the dead_members list, this is like... 5% safer than len() == 0
        # because it is looking at the list as a list rather than a property of it against an int
        core_io.send_output(
            {
                "message": f"{player_party_instance.name} has failed in their quest after {player_party_instance.progress * 10} miles"
            }
        )
    for player_instance in player_party_instance.members:
        player_report = +f"""
    Player Name: {player_instance.name}
    Player Base Health: {player_instance.base_health}                             
    Player Final Health: {player_instance.health}
    Player Int: {player_instance.intellect}
    Player Str: {player_instance.strength}
    Player Agl: {player_instance.agility}
    Player Lck: {player_instance.luck}
    Player Gold: {player_instance.inventory.gold}
    Player Potions: {player_instance.inventory.potions}
    Player Attack Name: {player_instance.attack_name}
    Player Attack Power: {player_instance.attack_power}
    """

    player_report += "Fallen Members\n\n"
    for player_instance in player_party_instance.dead_members:
        player_report += f"""
    Player Name: {player_instance.name}
    Player Base Health: {player_instance.base_health}                             
    Player Final Health: {player_instance.health}
    Player Int: {player_instance.intellect}
    Player Str: {player_instance.strength}
    Player Agl: {player_instance.agility}
    Player Lck: {player_instance.luck}
    Player Gold: {player_instance.inventory.gold}
    Player Potions: {player_instance.inventory.potions}
    Player Attack Name: {player_instance.attack_name}
    Player Attack Power: {player_instance.attack_power}
    """

    core_io.send_output({"message": f"{player_report}"})


__all__ = ["RPyGInterface", "launch_game", "ContentPaths"]
