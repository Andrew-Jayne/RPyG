from interaction.interaction import Interaction
from message.message import Message
from logic.logic import select_combat_target
from combat.combat_actions import attack, evade, post_battle

# Only for Type Checking
from actors.actor_party import PlayerParty, EnemyParty

#Battle Flow:
    #Player Party Attacks Enemy
    #Enemy Party Attacks  Player Party
# this function makes Linus Torvalds sad, make it better



class Combat:
    def battle(player_party_instance:PlayerParty, enemy_party_instance:EnemyParty) -> None:
        if not isinstance(player_party_instance, PlayerParty):
            raise ValueError("The 'player_party_instance' parameter must be of type PlayerParty. Received type: {}".format(type(player_party_instance).__name__))
        if not isinstance(enemy_party_instance, EnemyParty):
            raise ValueError("The 'enemy_party_instance' parameter must be of type PlayerParty. Received type: {}".format(type(enemy_party_instance).__name__))
        

        Message.battle_start_message()
        battle_complete = False
        while battle_complete == False:
            Message.battle_hud_message(player_party_instance, enemy_party_instance)

            # Players Attack
            if len(enemy_party_instance.members) == 0:
                # End Battle if all Enemies are dead
                battle_complete = True
                break

            if battle_complete == False:
                for player_instance in player_party_instance.members:

                    ## Evalute if members are poisioned and damage accordingly
                    if player_instance.is_poisioned == True:
                        Message.poison_damage_message(player_instance)
                        player_instance.damage(player_instance.poison_damage)

                    if len(enemy_party_instance.members) == 0:
                        # End Battle if all Enemies are dead
                        battle_complete = True
                        break
                    else:
                        match Interaction.in_battle(player_instance):
                            case "ATTACK": #select target
                                target_index = int(Interaction.choose_combat_target(enemy_party_instance))
                                enemy_instance = enemy_party_instance.members[target_index]

                                attack(attacker_instance=player_instance, target_instance=enemy_instance)
                                if enemy_instance.health == 0:
                                    Message.defeated_message(enemy_instance.name)
                                    enemy_party_instance.lose_member(enemy_instance)
                            case "EVADE":
                                Message.evade_prep_message(player_instance.name)
                                player_instance.will_evade = True
                            case "HEAL":
                                player_instance.use_potion()
                        

            # Enemies Attack
            if battle_complete == False:
                if len(player_party_instance.members) == 0:
                    # End Battle if All Players are dead
                    battle_complete = True
                    break
                else:
                    for enemy_instance in enemy_party_instance.members:

                        ## Evalute if members are poisioned and damage accordingly
                        if enemy_instance.is_poisioned == True:
                            Message.poison_damage_message(enemy_instance)
                            enemy_instance.damage(enemy_instance.poison_damage)

                        if len(player_party_instance.members) == 0:
                            # End Battle if All Players are dead
                            battle_complete = True
                            break

                        else:
                            target_index = select_combat_target(player_party_instance)
                            target_player = player_party_instance.members[target_index]

                            if target_player.will_evade == True:
                                if evade(target_player) == True:
                                    Message.evade_success_message(player_instance.name)
                                    target_player.will_evade = False
                                else:
                                    Message.evade_failure_message(player_instance.name)
                                    attack(attacker_instance=enemy_instance, target_instance=target_player)
                                    target_player.will_evade = False   
                            else:
                                attack(attacker_instance=enemy_instance, target_instance=target_player)

                            if target_player.health == 0:
                                Message.defeated_message(target_player.name)
                                player_party_instance.lose_member(target_player)    

        ## Display Victory Message if players do not die
        if len(player_party_instance.members) != 0 and len(enemy_party_instance.members) == 0 and battle_complete == True:
            Message.defeated_message(enemy_party_instance.name)
            post_battle(player_party_instance)