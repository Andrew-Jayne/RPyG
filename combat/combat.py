from interaction.interaction import Interaction
from display.display import Display
from message.message import Message
from combat.combat_attacks import attack
import random
import pickle

class Combat:

    @staticmethod
    def battle(player_instance, enemy_instance):
        Display.clear_display()
        Message.battle_start_message()
        while enemy_instance.health != 0:
            Message.battle_hud_message(player_instance=player_instance, enemy_instance=enemy_instance)
            match Interaction.in_battle(player_instance):
                case "ATTACK":
                      if Interaction.global_game_mode == "MANUAL":
                        Display.clear_display()
                      attack(attacker_instance=player_instance, target_instance=enemy_instance)
                case "HEAL":
                    if Interaction.global_game_mode == "MANUAL":
                        Display.clear_display()
                    player_instance.use_potion()
            ## End Battle If Enemy dies
            if enemy_instance.health == 0:
                break
            
            ## Follower Actions
            if player_instance.has_follower == True:
                follower_action = Interaction.in_battle(player_instance.follower_instance)
                match follower_action:
                    case "ATTACK":
                        attack(attacker_instance=player_instance.follower_instance, target_instance=enemy_instance)
                    case "HEAL":
                        player_instance.follower_instance.use_potion()
            
            ## Enemy Attacks
            if player_instance.has_follower == True:
                set_target = random.randint(0,1)
                if set_target == 0:
                    target = player_instance
                elif set_target == 1:
                    target = player_instance.follower_instance
            else:
                target = player_instance
            attack(attacker_instance=enemy_instance, target_instance=target)
            ## Remove Follower if they die
            if player_instance.has_follower == True:
                if player_instance.follower_instance.health == 0:
                    player_instance.lose_follower(player_instance.follower_instance)
            ## End combat if player dies
            if player_instance.health == 0:
                break

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
            Display.clear_display()