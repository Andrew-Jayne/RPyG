from interaction import Interaction

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
            ## End Battle If player dies
            if enemy_instance.health == 0:
                break

            ## Enemy Attacks
            __class__._enemy_attack(player_instance, enemy_instance)
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
        print(f"You Attack with {player_instance.attack_name} and inflict {player_instance.attack_power} damage")
        enemy_instance.damage(player_instance.attack_power)
        print(f"{enemy_instance.name} has {enemy_instance.health} health remaining", end='\n\n')

    def _enemy_attack(player_instance, enemy_instance):
        print(f"{enemy_instance.name} attacks you with {enemy_instance.attack_name} inflicting {enemy_instance.attack_power} damage")
        player_instance.damage(enemy_instance.attack_power)
        print(f"You have {player_instance.health} Health remaining", end='\n\n') 
