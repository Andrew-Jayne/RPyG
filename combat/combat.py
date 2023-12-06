import random

from interaction.interaction import Interaction
from display.display import Display
from message.message import Message
from combat.combat_actions import attack, evade, post_battle

#Battle Flow:
    #Player  Attacks Enemy
    #Follower  Attacks Enemy
    #Enemy Attacks Player or Follower


class Combat:
    def battle(player_party_instance, enemy_party_instance):
        Message.battle_start_message()
        battle_complete = False
        while battle_complete == False:
            if battle_complete == False:
                for player_instance in player_party_instance.members:
                    if len(enemy_party_instance.members) != 0:
                        match Interaction.in_battle(player_instance):
                            case "ATTACK": #select target
                                target_index = int(Interaction.choose_combat_target(enemy_party_instance))
                                try:
                                    enemy_instance = enemy_party_instance.members[target_index]
                                except:
                                    import pdb; pdb.set_trace()

                                attack(attacker_instance=player_instance, target_instance=enemy_instance)
                                if enemy_instance.health == 0:
                                    enemy_party_instance.lose_member(enemy_instance)
                            case "EVADE":
                                Message.evade_prep_message() # this is going to be so broken I need to write the attepmt evade flag to the instance 
                                player_instance.will_evade = True
                            case "HEAL":
                                player_instance.use_potion()
                    else:
                        battle_complete = True
                    ## End Battle if all enemies are defeated
            else:
                battle_complete = True

                if  battle_complete == False:
                    if len(player_party_instance.members) != 0:
                        for enemy_instance in enemy_party_instance.members:
                                target_max_index = len(player_party_instance.members) - 1 
                                target_index = int(random.randint(0,target_max_index))
                                target_player = player_party_instance.members[target_index]
                                if target_player.will_evade == True:
                                    if evade(target_player) == False:
                                        Message.evade_failure_message()
                                        attack(attacker_instance=enemy_instance, target_instance=target_player)
                                    else:
                                        Message.evade_success_message()
                                else:
                                    attack(attacker_instance=enemy_instance, target_instance=target_player)
                                if target_player.health == 0:
                                    player_party_instance.lose_member(target_player)
                    else:
                        battle_complete = True
                    ## End Battle if Everyone dies
                else:
                    battle_complete = True

        ## Display Victory Message if player does not die
        if len(player_party_instance.members) != 0 and len(enemy_party_instance.members) == 0 and battle_complete == True:
            Message.defeated_message("Andrew put a name on the enemy groups to fix this :)") #hack while I make better groups
            post_battle(player_party_instance)