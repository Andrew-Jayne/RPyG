from interaction import Interaction
import random

class Combat:
    def __init__(self, player_instance, enemy_instance):
        self.player_instance = player_instance
        self.enemy_instance = enemy_instance
    
    def battle(player_instance, enemy_instance):
        while enemy_instance.health != 0:
            player_action = Interaction.in_battle(player_instance)
            match player_action:
                case "ATTACK":
                      __class__._player_attack(player_instance, enemy_instance)
                case "HEAL":
                    player_instance.use_potion()
            ## End Battle If Enemy dies
            if enemy_instance.health == 0:
                break
            
            ## Follower Actions
            if player_instance.has_follower == True:
                follower_action = Interaction.in_battle(player_instance.follower_instance)
                match follower_action:
                    case "ATTACK":
                        __class__._follower_attack(player_instance.follower_instance, enemy_instance)
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
            
            __class__._enemy_attack(target, enemy_instance)
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
            print(f"{enemy_instance.name} has been defeated!", end='\n\n')
            while player_post_action != "TRAVEL":
                player_post_action = Interaction.post_battle(player_instance)
                if player_post_action == "HEAL":
                    player_instance.use_potion()



    ## Hidden Methods
    def _player_attack(player_instance, enemy_instance):
        if __class__._check_for_critical(player_instance) == True:
            print(f"You Attack with {player_instance.attack_name} and inflict {player_instance.attack_power * 2} damage")
            enemy_instance.damage(player_instance.attack_power * 2)
            print(f"{player_instance.name} got a critical hit!!")
        else:
            print(f"You Attack with {player_instance.attack_name} and inflict {player_instance.attack_power} damage")
            enemy_instance.damage(player_instance.attack_power)
        print(f"{enemy_instance.name} has {enemy_instance.health} health remaining", end='\n\n')

    def _enemy_attack(player_instance, enemy_instance):
        if __class__._check_for_critical(enemy_instance) == True:
            print(f"{enemy_instance.name} attacks with {enemy_instance.attack_name} inflicting {enemy_instance.attack_power * 2} damage")
            print(f"{enemy_instance.name} got a critical hit!!")
            player_instance.damage(enemy_instance.attack_power)
        else:
            print(f"{enemy_instance.name} attacks with {enemy_instance.attack_name} inflicting {enemy_instance.attack_power} damage")
            player_instance.damage(enemy_instance.attack_power)
        print(f"{player_instance.name} has {player_instance.health} Health remaining", end='\n\n') 

    def _follower_attack(follower_instance, enemy_instance):
        if __class__._check_for_critical(follower_instance) == True:
            print(f"{follower_instance.name} Attacks with {follower_instance.attack_name} and inflicts {follower_instance.attack_power * 2} damage")
            enemy_instance.damage(follower_instance.attack_power * 2)
            print(f"{follower_instance.name} got a critical hit!!")
        else:
            print(f"{follower_instance.name} Attacks with {follower_instance.attack_name} and inflicts {follower_instance.attack_power} damage")
            enemy_instance.damage(follower_instance.attack_power)
        print(f"{enemy_instance.name} has {enemy_instance.health} health remaining", end='\n\n')

    @staticmethod
    def _check_for_critical(combatant_instance):
        crit_check = random.randint(1,100)
        if crit_check <= combatant_instance.luck:
            return True
        else:
            return False