
class Combat:
    def __init__(self, player_instance, enemy_instance):
        self.player_instance = player_instance
        self.enemy_instance = enemy_instance


    def set_player_attack(player_instance): #need to make a proper table.
        if player_instance.strength > player_instance.intellect:
            player_attack_power:int = player_instance.strength
            player_instance.attack = "Sword Strike"
        elif player_instance.strength == 1 and player_instance.intellect == 1:
            player_instance.attack = "Clumsy Punch"
        else:
            player_attack_power:int = player_instance.intellect
            player_instance.attack = "Arcane Blast"
        
        return player_attack_power

    def set_enemy_attack(enemy_instance):
        if enemy_instance.strength > enemy_instance.intellect:
            enemy_attack_power:int = enemy_instance.strength
        else:
            enemy_attack_power:int = enemy_instance.intellect

        return enemy_attack_power
    
    def combat (player_instance, enemy_instance):

        player_attack_power = __class__.set_player_attack(player_instance)
        enemy_attack_power = __class__.set_enemy_attack(enemy_instance)

        while enemy_instance.health != 0:
  
            ## Check if the player should use a health potion
            if player_instance.health <= 8 and player_instance.potions != 0:
                player_instance.potions -= 1
                player_instance.heal(5)
                print(f"You consume a health potion and heal 5 points")
                print(f"You have {player_instance.potions} Potions Remaining")
            else:
                if player_instance.potions == 0 and player_instance.health <= 8:
                    print("You have no remaining potions and must make a stand!")
            ## Player Attacks if they did not drink a potion
                enemy_instance.damage(player_attack_power)
                print(f"You Attack with {player_instance.attack} and inflict {player_attack_power} damage")
                print(f"The {enemy_instance.name} has {enemy_instance.health} health remaining")
            if enemy_instance.health == 0:
                break

            ## Enemy Attacks
            player_instance.damage(enemy_attack_power)
            print(f"The {enemy_instance.name} attacks you with {enemy_instance.attack} inflicting {enemy_attack_power} damage")
            print(f"You have {player_instance.health} Health remaining")  
            if player_instance.health == 0:
                break   

        ## Display Victory Message
        if player_instance.health != 0 and enemy_instance.health == 0:
            print(f"The {enemy_instance.name} has been defeated!")
