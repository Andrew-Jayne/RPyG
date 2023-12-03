import random
import pickle
from interaction.interaction import Interaction
from display.display import Display
from message.message import Message
from combat.combat_actions import attack, evade

#Battle Flow:
    #Player  Attacks Enemy
    #Follower  Attacks Enemy
    #Enemy Attacks Player or Follower


class Combat:

    def battle(player_instance, enemy_instance):
        Message.battle_start_message()
        battle_complete = False
        playable_charcters_list = [player_instance]
        if player_instance.has_follower == True:
            playable_charcters_list.append(player_instance.follower_instance)
        for playable_instance in playable_charcters_list:
            print(f"{playable_instance.name}: {playable_instance.health}")
        print(f"{enemy_instance.name}: {enemy_instance.health}", end="\n\n\n")

        while battle_complete == False:

            attempt_evade = False ## need to make this an option per playable instance, and store it somewhere (maybe make each turn of combat an instance of class?)

            ## Player & Follower Attack
            for playable_instance in playable_charcters_list:
                if battle_complete == False:
                    match Interaction.in_battle(player_instance):
                        case "ATTACK":
                            attack(attacker_instance=playable_instance, 
                                   target_instance=enemy_instance)
                        case "EVADE":
                            Message.evade_prep_message()
                            attempt_evade = True
                        case "HEAL":
                            playable_instance.use_potion()
                    ## End Battle If Enemy dies
                    if enemy_instance.health == 0:
                        battle_complete = True
            
            ## Enemy Attacks
            if battle_complete == False:
                target = playable_charcters_list[random.randint(0,(len(playable_charcters_list) -1))]
                if attempt_evade == True and evade(target) == True:
                    Message.evade_sucess_message()
                elif attempt_evade == True and evade(target) == False:
                    Message.evade_failure_message()
                    attack(attacker_instance=enemy_instance, target_instance=target)
                else:
                    attack(attacker_instance=enemy_instance, target_instance=target)

            ## Remove Follower if they die
            if player_instance.has_follower == True:
                if player_instance.follower_instance.health == 0:
                    player_instance.lose_follower(player_instance.follower_instance)
            ## End combat if player dies
            if player_instance.health == 0:
                battle_complete = True

        ## Display Victory Message if player does not die
        player_post_action = ""
        if player_instance.health != 0 and enemy_instance.health == 0:
            Message.defeated_message(enemy_instance.name)
            while player_post_action != "TRAVEL":
                player_post_action = Interaction.post_battle(player_instance)
                if player_post_action == "HEAL":
                    player_instance.use_potion()
                if player_post_action == "SAVE":
                    # Open the file in write mode. If the file doesn't exist, it will be created.
                    # If it does exist, it will be overwritten.
                    with open('savegame.rpygs', 'wb') as save_file:
                        # Write some text to the file.
                        pickle.dump(player_instance, save_file)
                        print(f"Successfully Saved Game for: {player_instance.name}")
                        exit()
                        # The file is automatically closed when you exit the 'with' block.