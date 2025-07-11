# Only for Type Checking
from actors import CombatantParty, Enemy, EnemyParty, PlayableActor, PlayerParty
from gameState.file import save_game
from interaction.interaction import Interaction
from message.message import Message
from utilites.utilities import ensure_type


def is_party_alive(party_instance: CombatantParty) -> bool:
    ensure_type(party_instance, CombatantParty, "party_instance")

    if len(party_instance.members) <= 0:
        return False
    else:
        return True


def clear_dead_members(party_instance: CombatantParty) -> None:
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

    # Check if players have died
    if is_party_alive(player_party_instance) is False:
        battle_complete = True
        return True
    elif is_party_alive(enemy_party_instance) is False:
        battle_complete = True
        return True
    else:
        return False


def process_player_turn(
    player_party_instance: PlayerParty, enemy_party_instance: EnemyParty
) -> None:
    ensure_type(player_party_instance, PlayerParty, "player_party_instance")
    ensure_type(enemy_party_instance, EnemyParty, "enemy_party_instance")

    for player_instance in player_party_instance.members:
        if is_party_alive(enemy_party_instance) is True:
            match Interaction.in_battle(player_instance):
                case "ATTACK":  # select target
                    target_index = player_instance.select_combat_target(
                        enemy_party_instance
                    )
                    enemy_instance: Enemy = enemy_party_instance.members[target_index]
                    player_instance.attack(enemy_instance)
                    if enemy_instance.health == 0:
                        Message.defeated_message(enemy_instance.name)
                        enemy_party_instance.lose_member(enemy_instance)

                case player_instance.special_attack_name:
                    player_instance.special_attack(
                        player_instance, enemy_party_instance
                    )
                    for enemy_instance in enemy_party_instance.members:
                        if enemy_instance.health == 0:
                            Message.defeated_message(enemy_instance.name)
                            enemy_party_instance.lose_member(enemy_instance)

                case player_instance.react_action:
                    Message.display_message(
                        player_instance.react_messages["prep_message"],
                        new_line_count=2,
                    )
                    player_instance.will_react = True

                case "HEAL":
                    player_instance.use_potion()
            clear_dead_members(enemy_party_instance)
        else:
            break


def process_enemy_turn(
    player_party_instance: PlayerParty,
    enemy_party_instance: EnemyParty,
) -> None:
    ensure_type(player_party_instance, PlayerParty, "player_party_instance")
    ensure_type(enemy_party_instance, EnemyParty, "enemy_party_instance")

    for enemy_instance in enemy_party_instance.members:
        if is_party_alive(player_party_instance) is True:
            target_index = enemy_instance.select_combat_target(player_party_instance)
            target_player: PlayableActor = player_party_instance.members[target_index]

            if target_player.will_react is True:
                if target_player.react() is True:
                    Message.display_message(
                        target_player.react_messages["success_message"],
                        new_line_count=2,
                    )
                else:
                    Message.display_message(
                        target_player.react_messages["failure_message"],
                        new_line_count=2,
                    )
                    enemy_instance.attack(
                        target_instance=target_player,
                    )

                target_player.will_react = False
            else:
                enemy_instance.attack(target_instance=target_player)

            if target_player.health == 0:
                Message.defeated_message(target_player.name)
                player_party_instance.lose_member(target_player)
            clear_dead_members(player_party_instance)
        else:
            break


def process_turn(
    attacker_party_instance: CombatantParty,
    defender_party_instance: CombatantParty,
) -> None:
    ensure_type(attacker_party_instance, CombatantParty, "attacker_party_instance")
    ensure_type(defender_party_instance, CombatantParty, "defender_party_instance")

    for attacker_instance in attacker_party_instance.members:
        target_index = attacker_instance.select_combat_target(defender_party_instance)
        attacker_instance.attack(defender_party_instance.members[target_index])


def post_battle(player_party_instance: PlayerParty) -> None:
    ensure_type(player_party_instance, PlayerParty, "player_party_instance")

    player_post_action = ""
    while player_post_action != "TRAVEL":
        player_post_action = Interaction.post_battle(player_party_instance)
        if player_post_action == "HEAL":
            for member_instance in player_party_instance.members:
                member_instance.use_potion()
        if player_post_action == "SAVE":
            save_game(player_party_instance)


def battle(
    player_party_instance: PlayerParty,
    enemy_party_instance: EnemyParty,
) -> bool:
    ensure_type(player_party_instance, PlayerParty, "player_party_instance")
    ensure_type(enemy_party_instance, EnemyParty, "enemy_party_instance")

    Message.battle_start_message()
    battle_complete = False
    while battle_complete is False:
        Message.battle_hud_message(player_party_instance, enemy_party_instance)

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
        is_party_alive(player_party_instance) is True
        and is_party_alive(enemy_party_instance) is False
        and battle_complete is True
    ):
        Message.defeated_message(enemy_party_instance.name)
        post_battle(player_party_instance)
        return True
    else:
        return False
