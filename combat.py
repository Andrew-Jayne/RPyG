
class Combat:
    def __init__(self, player_instance, enemy_instance):
        self.player_instance = player_instance
        self.enemy_instance = enemy_instance
    
    def combat (player_instance, enemy_instance):

        player_attack_power = player_instance.set_player_attack_power()
        player_attack_name = player_instance.set_player_attack_name()
        enemy_attack_power = enemy_instance.set_enemy_attack_power()

        while enemy_instance.health != 0:
  
            ## Check if the player should use a health potion
            if player_instance.health <= 8 and player_instance.potions != 0:
                player_instance.use_potion()
            else:
                if player_instance.potions == 0 and player_instance.health <= 8:
                    print("You have no remaining potions and must make a stand!")
            ## Player Attacks if they did not drink a potion
                print(f"You Attack with {player_attack_name} and inflict {player_attack_power} damage")
                enemy_instance.damage(player_attack_power)
                print(f"{enemy_instance.name} has {enemy_instance.health} health remaining", end='\n\n')
            if enemy_instance.health == 0:
                break

            ## Enemy Attacks
            print(f"{enemy_instance.name} attacks you with {enemy_instance.attack_name} inflicting {enemy_attack_power} damage")
            player_instance.damage(enemy_attack_power)
            print(f"You have {player_instance.health} Health remaining", end='\n\n')  
            if player_instance.health == 0:
                break   

        ## Display Victory Message
        if player_instance.health != 0 and enemy_instance.health == 0:
            print(f"{enemy_instance.name} has been defeated!", end='\n\n')
