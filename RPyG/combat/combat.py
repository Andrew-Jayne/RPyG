from RPyG.constructs import (
    CombatantParty,
    CombatantType,
    EnemyActor,
    PlayableActor,
)
from RPyG.core_io import input_models, output_models
from RPyG.utilities import ensure_type


def clear_dead_members(party_instance: CombatantParty[CombatantType]) -> None:
    ensure_type(party_instance, CombatantParty, "party_instance")
    for member in party_instance.members:
        if member.health == 0:
            party_instance.lose_member(member)


def is_battle_complete() -> bool:
    from RPyG.game_state import GameState

    game_state = GameState.get_game_state()
    with game_state.borrow_enemy_party() as enemy_party:
        if game_state.player_party.members == [] or enemy_party.members == []:
            return True
        return False


def process_player_turn() -> None:
    from RPyG.core_io import CoreIO
    from RPyG.game_state import GameState

    core_io = CoreIO.get_core_io()

    game_state = GameState.get_game_state()
    with game_state.borrow_enemy_party() as enemy_party:
        ## Gross Code Dupe, but this whole function sucks ass
        for player_instance in game_state.player_party.members:
            if enemy_party.members != []:
                core_io.request_input(
                    input_models.UserPromptRequest(
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
                if (
                    battle_choice == "HEAL"
                    and player_instance.is_fully_healed() is True
                ):
                    core_io.send_output(
                        output_models.OutputMessage(
                            f"{player_instance.name} is fully healed, it would be unwise to use a potion"
                        )
                    )
                    core_io.request_input(
                        input_models.UserPromptRequest(
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
                            output_models.OutputMessage(
                                "Stubborn aren't you, fine waste the damn potion"
                            )
                        )
                match battle_choice:
                    case "ATTACK":  # select target
                        target_index = player_instance.select_combat_target(enemy_party)
                        enemy_instance: EnemyActor = enemy_party.members[target_index]
                        player_instance.attack(enemy_instance)
                        if enemy_instance.health == 0:
                            enemy_party.lose_member(enemy_instance)

                    case player_instance.special_attack_name:
                        player_instance.special_attack(enemy_party)
                        for enemy_instance in enemy_party.members:
                            if enemy_instance.health == 0:
                                enemy_party.lose_member(enemy_instance)

                    case player_instance.react_action:
                        core_io.send_output(
                            output_models.OutputMessage(
                                player_instance.react_messages["prep_message"]
                            )
                        )
                        player_instance.will_react = True

                    case "HEAL":
                        player_instance.use_potion()
                    case _:
                        raise ValueError(f"Invalid player_action {battle_choice}")

                clear_dead_members(enemy_party)
            else:
                break


def process_enemy_turn() -> None:
    from RPyG.core_io import CoreIO
    from RPyG.game_state import GameState

    core_io = CoreIO.get_core_io()

    game_state = GameState.get_game_state()
    with game_state.borrow_enemy_party() as enemy_party:
        for enemy_instance in enemy_party.members:
            if game_state.player_party.members != []:
                target_index = enemy_instance.select_combat_target(
                    game_state.player_party
                )
                target_player: PlayableActor = game_state.player_party.members[
                    target_index
                ]

                if target_player.will_react is True:
                    if target_player.react() is True:
                        core_io.send_output(
                            output_models.OutputMessage(
                                target_player.react_messages["success_message"]
                            )
                        )
                    else:
                        core_io.send_output(
                            output_models.OutputMessage(
                                target_player.react_messages["failure_message"]
                            )
                        )
                        enemy_instance.attack(
                            target_instance=target_player,
                        )

                    target_player.will_react = False
                else:
                    enemy_instance.attack(target_instance=target_player)

                if target_player.health == 0:
                    game_state.player_party.lose_member(target_player)
                clear_dead_members(game_state.player_party)
            else:
                break


def post_battle() -> None:
    from RPyG.core_io import CoreIO
    from RPyG.game_state import GameState

    core_io = CoreIO.get_core_io()
    game_state = GameState.get_game_state()

    player_post_action = ""
    while player_post_action != "TRAVEL":
        core_io.request_input(
            input_models.UserPromptRequest(
                prompts=["Choose an Action:"],
                options=["HEAL", "TRAVEL", "SAVE"],
            )
        )
        player_post_action = core_io.receive_input()
        if player_post_action == "HEAL":
            for member_instance in game_state.player_party.members:
                member_instance.use_potion()
        if player_post_action == "SAVE":
            core_io.interface.save_game_state(game_state)


def build_hud_data() -> str:
    from RPyG.game_state import GameState

    game_state = GameState.get_game_state()
    with game_state.borrow_enemy_party() as enemy_party:
        battle_hud_message = ""

        for playable_instance in game_state.player_party.members:
            battle_hud_message += (
                f"{playable_instance.name}: {playable_instance.health}"
            )
            battle_hud_message += "\n"
        battle_hud_message += "\n"

        for enemy_instance in enemy_party.members:
            battle_hud_message += f"{enemy_instance.name}: {enemy_instance.health}\n"
            battle_hud_message += "\n"

        battle_hud_message += "\n"

        return battle_hud_message


def battle() -> None:
    from RPyG.core_io import CoreIO
    from RPyG.game_state import GameState

    core_io = CoreIO.get_core_io()
    game_state = GameState.get_game_state()
    with game_state.borrow_enemy_party() as enemy_party:
        core_io.send_output(
            output_models.OutputMessage("The Battle Begins!", reset_display=True)
        )
        battle_complete = False
        while battle_complete is False:
            core_io.send_output(
                output_models.BattleHudMessage(message=build_hud_data())
            )

            ## Check if all parties are alive before running player turn
            if is_battle_complete() is False:
                process_player_turn()
            else:
                battle_complete = True

            ## Check if all parties are alive before running enemy turn
            if is_battle_complete() is False:
                process_enemy_turn()
            else:
                battle_complete = True

            ## Check if all parties are alive after both turns
            if is_battle_complete() is True:
                battle_complete = True

        ## If Battle is done, Player party is dead, and enemy party is not, return
        if (
            battle_complete is True
            and game_state.player_party.members == []
            and enemy_party.members != []
        ):
            return

    # the previous condition was inverted to allow the final reference to the borrowed
    # enemy party to be disposed of before reseting the instance
    # the only place enemy party is reset, because death is a game reset (for now)
    game_state.reset_enemy_party()
    post_battle()

    return
