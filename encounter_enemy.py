import random
from actor_enemy import Enemy
from combat import Combat
from display import Display
from interaction import Interaction

class EnemyEncounters():
    ## This can be rebuild to be more Dry there is a heap of redundant code here that can be improved, this will also be better for moving the enemies into lists, then eventually into a yaml file.
    @staticmethod
    def enemy_encounter(player_instance):
        enemy_chance = random.randint(0,4)
        if enemy_chance == 6:
            print("WTF, You're not supposed to see this, some kind of Cosmic bit flip happened")

        elif enemy_chance == 0 or enemy_chance == 1:
            small_enemy = Enemy(name="Feral Imp", health=8, strength=1, intellect=3, luck=4, attack_name="fireball")
            Display.encounter_message(small_enemy.name)
            player_action = Interaction.encounter_enemy()
            match player_action:
                case "ATTACK":
                      Combat.battle(player_instance, small_enemy)
                case "FLEE":
                    if player_instance.luck >= random.randint(4,15):
                        Display.flee_success_message(small_enemy.name)
                    else:
                        Display.flee_failure_message(small_enemy.name)
                        Combat.battle(player_instance, small_enemy)
            

        elif enemy_chance == 2 or enemy_chance == 3:
            medium_enemy = Enemy(name="Dire Wolf", health=15, strength=5, intellect=3, luck=6 ,attack_name="Wolf Bite")
            Display.encounter_message(medium_enemy.name)
            Combat.battle(player_instance, medium_enemy)

        elif enemy_chance == 4:
            large_enemy = Enemy(name="Cave Troll", health=30, strength=10, intellect=1, luck=2, attack_name="Club Smash")
            Display.encounter_message(large_enemy.name)
            Combat.battle(player_instance, large_enemy)


    ## Enemy lists
    small_enemies = {

    }

    medium_enemies = {

    }

    large_enemies = {

    }