# Only for Type Checking
from actors.actor_party import EnemyParty, Party, PlayerParty
from combat.combat_actions import attack, post_battle, react, special_attack
from interaction.interaction import Interaction
from logic.logic import select_combat_target
from message.message import Message
from utilites.utilities import ensure_type


class Combat:
    battle_complete = True

    @staticmethod
    def is_party_alive(party_instance: Party) -> bool:
        ensure_type(party_instance, Party, "party_instance")

        if len(party_instance.members) <= 0:
            return False
        else:
            return True

    @staticmethod
    def clear_dead_members(party_instance: Party) -> None:
        ensure_type(party_instance, Party, "party_instance")

        for member in party_instance.members:
            if member.health == 0:
                party_instance.lose_member(member)

    @staticmethod
    def is_battle_complete(
        player_party_instance: PlayerParty, enemy_party_instance: EnemyParty
    ) -> bool:
        ensure_type(player_party_instance, PlayerParty, "player_party_instance")
        ensure_type(enemy_party_instance, EnemyParty, "enemy_party_instance")

        # Check if players have died
        if __class__.is_party_alive(player_party_instance) is False:
            __class__.battle_complete = True
            return True
        elif __class__.is_party_alive(enemy_party_instance) is False:
            __class__.battle_complete = True
            return True
        else:
            return False

    @staticmethod
    def process_player_turn(
        player_party_instance: PlayerParty, enemy_party_instance: EnemyParty
    ) -> None:
        ensure_type(player_party_instance, PlayerParty, "player_party_instance")
        ensure_type(enemy_party_instance, EnemyParty, "enemy_party_instance")

        for player_instance in player_party_instance.members:
            if __class__.is_party_alive(enemy_party_instance) is True:
                match Interaction.in_battle(player_instance):
                    case "ATTACK":  # select target
                        target_index = Interaction.choose_combat_target(
                            enemy_party_instance
                        )
                        enemy_instance = enemy_party_instance.members[target_index]
                        attack(
                            attacker_instance=player_instance,
                            target_instance=enemy_instance,
                        )
                        if enemy_instance.health == 0:
                            Message.defeated_message(enemy_instance.name)
                            enemy_party_instance.lose_member(enemy_instance)

                    case player_instance.special_attack_name:
                        special_attack(player_instance, enemy_party_instance)
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
                __class__.clear_dead_members(enemy_party_instance)
            else:
                break

    @staticmethod
    def process_enemy_turn(
        player_party_instance: PlayerParty, enemy_party_instance: EnemyParty
    ) -> None:
        ensure_type(player_party_instance, PlayerParty, "player_party_instance")
        ensure_type(enemy_party_instance, EnemyParty, "enemy_party_instance")

        for enemy_instance in enemy_party_instance.members:
            if __class__.is_party_alive(player_party_instance) == True:
                target_index = select_combat_target(player_party_instance)
                target_player = player_party_instance.members[target_index]

                if target_player.will_react == True:
                    if react(target_player) == True:
                        Message.display_message(
                            target_player.react_messages["success_message"],
                            new_line_count=2,
                        )
                        target_player.will_react = False
                    else:
                        Message.display_message(
                            target_player.react_messages["failure_message"],
                            new_line_count=2,
                        )
                        attack(
                            attacker_instance=enemy_instance,
                            target_instance=target_player,
                        )
                        target_player.will_react = False
                else:
                    attack(
                        attacker_instance=enemy_instance, target_instance=target_player
                    )

                if target_player.health == 0:
                    Message.defeated_message(target_player.name)
                    player_party_instance.lose_member(target_player)
                __class__.clear_dead_members(player_party_instance)
            else:
                break

    @staticmethod
    def battle(
        player_party_instance: PlayerParty, enemy_party_instance: EnemyParty
    ) -> bool:
        ensure_type(player_party_instance, PlayerParty, "player_party_instance")
        ensure_type(enemy_party_instance, EnemyParty, "enemy_party_instance")

        Message.battle_start_message()
        __class__.battle_complete = False
        while __class__.battle_complete is False:
            Message.battle_hud_message(player_party_instance, enemy_party_instance)

            ## Check if all parties are alive before running player turn
            if (
                __class__.is_battle_complete(
                    player_party_instance, enemy_party_instance
                )
                is False
            ):
                __class__.process_player_turn(
                    player_party_instance, enemy_party_instance
                )

            ## Check if all parties are alive before running enemy turn
            if (
                __class__.is_battle_complete(
                    player_party_instance, enemy_party_instance
                )
                is False
            ):
                __class__.process_enemy_turn(
                    player_party_instance, enemy_party_instance
                )

            ## Check if all parties are alive after both turns
            __class__.is_battle_complete(player_party_instance, enemy_party_instance)

        ## Display Victory Message if players do not die
        if (
            __class__.is_party_alive(player_party_instance) is True
            and __class__.is_party_alive(enemy_party_instance) is False
            and __class__.battle_complete is True
        ):
            Message.defeated_message(enemy_party_instance.name)
            post_battle(player_party_instance)
            return True
        else:
            return False
