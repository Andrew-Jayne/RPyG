import random
from actor_enemy import Enemy
from combat import Combat

class EnemyEncounters():
    
    @staticmethod
    def enemy_encounter(player_instance):
        enemy_chance = random.randint(0,4)
        if enemy_chance == 6:
            print("WTF, You're not supposed to see this, some kind of Cosmic bit flip happened")

        elif enemy_chance == 0 or enemy_chance == 1:
            small_enemy = Enemy(name="Feral Imp", health=8, strength=1, intellect=3, luck=4, attack_name="fireball")
            print(f"You encounter a {small_enemy.name}!")
            Combat.battle(player_instance, small_enemy)

        elif enemy_chance == 2 or enemy_chance == 3:
            medium_enemy = Enemy(name="Dire Wolf", health=15, strength=5, intellect=3, luck=6 ,attack_name="Wolf Bite")
            print(f"You encounter a {medium_enemy.name}!")
            Combat.battle(player_instance, medium_enemy)

        elif enemy_chance == 4:
            large_enemy = Enemy(name="Cave Troll", health=30, strength=10, intellect=1, luck=2, attack_name="Club Smash")
            print(f"You encounter a {large_enemy.name}!")
            Combat.battle(player_instance, large_enemy)


    ## Enemy lists
    small_enemies = {

    }

    medium_enemies = {

    }

    large_enemies = {

    }