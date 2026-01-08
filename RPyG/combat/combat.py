from RPyG.actors import (
    CombatantParty,
    CombatantType,
    Enemy,
    EnemyParty,
    PlayableActor,
    PlayerParty,
)
from RPyG.core_io import CoreIO
from RPyG.core_io.io_models import BattleHudMessage, OutputMessage, UserPromptRequest
from RPyG.game_state.file import save_game
from RPyG.utilities import ensure_type


def clear_dead_members(party_instance: CombatantParty[CombatantType]) -> None:
    ensure_type(party_instance, CombatantParty, "party_instance")
    for member in party_instance.members:
        if member.health == 0:
            party_instance.lose_member(member)


def is_battle_complete(
    player_party_instance: PlayerParty,
    enemy_party_instance: EnemyParty,
) -> bool:
    ensure_type(player_party_instance, PlayerParty, "player_party_instance")
    ensure_type(enemy_party_instance, EnemyParty, "enemy_party_instance")

    if player_party_instance.members == [] or enemy_party_instance.members == []:
        return True
    return False


def process_player_turn(
    player_party_instance: PlayerParty,
    enemy_party_instance: EnemyParty,
) -> None:
    core_io = CoreIO.get_core_io()

    ensure_type(player_party_instance, PlayerParty, "player_party_instance")
    ensure_type(enemy_party_instance, EnemyParty, "enemy_party_instance")

    ## Gross Code Dupe, but this whole function sucks ass
    for player_instance in player_party_instance.members:
        if enemy_party_instance.members != []:
            core_io.request_input(
                UserPromptRequest(
                    prompts=[f"{player_instance.name}", "Choose an Action:"],
                    options=[
                        "ATTACK",
                        f"{player_instance.special_attack_name}",
                        f"{player_instance.react_action}",
                        "HEAL",
                    ],
                )
            )
            battle_choice = core_io.receive_input()
            if battle_choice == "HEAL" and player_instance.is_fully_healed() is True:
                core_io.send_output(
                    OutputMessage(
                        f"{player_instance.name} is fully healed, it would be unwise to use a potion"
                    )
                )
                core_io.request_input(
                    UserPromptRequest(
                        prompts=[f"{player_instance.name}", "Choose an Action:"],
                        options=[
                            "ATTACK",
                            f"{player_instance.special_attack_name}",
                            f"{player_instance.react_action}",
                            "HEAL",
                        ],
                    )
                )
                battle_choice = core_io.receive_input()
                if battle_choice == "HEAL":
                    core_io.send_output(
                        OutputMessage("Stubborn aren't you, fine waste the damn potion")
                    )
            match battle_choice:
                case "ATTACK":  # select target
                    target_index = player_instance.select_combat_target(
                        enemy_party_instance
                    )
                    enemy_instance: Enemy = enemy_party_instance.members[target_index]
                    player_instance.attack(enemy_instance)
                    if enemy_instance.health == 0:
                        enemy_party_instance.lose_member(enemy_instance)

                case player_instance.special_attack_name:
                    player_instance.special_attack(enemy_party_instance)
                    for enemy_instance in enemy_party_instance.members:
                        if enemy_instance.health == 0:
                            enemy_party_instance.lose_member(enemy_instance)

                case player_instance.react_action:
                    core_io.send_output(
                        OutputMessage(player_instance.react_messages["prep_message"])
                    )
                    player_instance.will_react = True

                case "HEAL":
                    player_instance.use_potion()
                case _:
                    raise ValueError(f"Invalid player_action {battle_choice}")

            clear_dead_members(enemy_party_instance)
        else:
            break


def process_enemy_turn(
    player_party_instance: PlayerParty,
    enemy_party_instance: EnemyParty,
) -> None:
    core_io = CoreIO.get_core_io()
    ensure_type(player_party_instance, PlayerParty, "player_party_instance")
    ensure_type(enemy_party_instance, EnemyParty, "enemy_party_instance")

    for enemy_instance in enemy_party_instance.members:
        if player_party_instance.members != []:
            target_index = enemy_instance.select_combat_target(player_party_instance)
            target_player: PlayableActor = player_party_instance.members[target_index]

            if target_player.will_react is True:
                if target_player.react() is True:
                    core_io.send_output(
                        OutputMessage(target_player.react_messages["success_message"])
                    )
                else:
                    core_io.send_output(
                        OutputMessage(target_player.react_messages["failure_message"])
                    )
                    enemy_instance.attack(
                        target_instance=target_player,
                    )

                target_player.will_react = False
            else:
                enemy_instance.attack(target_instance=target_player)

            if target_player.health == 0:
                player_party_instance.lose_member(target_player)
            clear_dead_members(player_party_instance)
        else:
            break


def post_battle(player_party_instance: PlayerParty) -> None:
    ensure_type(player_party_instance, PlayerParty, "player_party_instance")
    core_io = CoreIO.get_core_io()

    player_post_action = ""
    while player_post_action != "TRAVEL":
        core_io.request_input(
            UserPromptRequest(
                prompts=["Choose an Action:"],
                options=["HEAL", "TRAVEL", "SAVE"],
            )
        )
        player_post_action = core_io.receive_input()
        if player_post_action == "HEAL":
            for member_instance in player_party_instance.members:
                member_instance.use_potion()
        if player_post_action == "SAVE":
            save_game(player_party_instance)


def build_hud_data(
    player_party_instance: PlayerParty,
    enemy_party_instance: EnemyParty,
) -> str:
    battle_hud_message = ""

    for playable_instance in player_party_instance.members:
        battle_hud_message += f"{playable_instance.name}: {playable_instance.health}"
        battle_hud_message += "\n"
    battle_hud_message += "\n"

    for enemy_instance in enemy_party_instance.members:
        battle_hud_message += f"{enemy_instance.name}: {enemy_instance.health}\n"
        battle_hud_message += "\n"

    battle_hud_message += "\n"

    return battle_hud_message


def battle(
    player_party_instance: PlayerParty,
    enemy_party_instance: EnemyParty,
) -> None:
    ensure_type(player_party_instance, PlayerParty, "player_party_instance")
    ensure_type(enemy_party_instance, EnemyParty, "enemy_party_instance")

    core_io = CoreIO.get_core_io()

    core_io.send_output(OutputMessage("The Battle Begins!"))
    battle_complete = False
    while battle_complete is False:
        core_io.send_output(
            BattleHudMessage(
                message=build_hud_data(
                    player_party_instance,
                    enemy_party_instance,
                )
            )
        )

        ## Check if all parties are alive before running player turn
        if is_battle_complete(player_party_instance, enemy_party_instance) is False:
            process_player_turn(player_party_instance, enemy_party_instance)
        else:
            battle_complete = True

        ## Check if all parties are alive before running enemy turn
        if is_battle_complete(player_party_instance, enemy_party_instance) is False:
            process_enemy_turn(player_party_instance, enemy_party_instance)
        else:
            battle_complete = True

        ## Check if all parties are alive after both turns
        if is_battle_complete(player_party_instance, enemy_party_instance) is True:
            battle_complete = True

    ## Display Victory Message if players do not die
    if (
        battle_complete is True
        and player_party_instance.members != []
        and enemy_party_instance.members == []
    ):
        post_battle(player_party_instance)
    return
