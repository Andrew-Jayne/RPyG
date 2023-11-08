import random
from actor_enemy import Enemy
from combat import Combat
from display import Display
from interaction import Interaction

class EnemyEncounters():
    ## This can be rebuild to be more Dry there is a heap of redundant code here that can be improved, this will also be better for moving the enemies into lists, then eventually into a yaml file.
            ## Enemy lists
    small_enemies = [
        {
            "name": "Feral Imp",
            "health": 8,
            "strength": 1,
            "intellect": 3,
            "luck": 4,
            "attack_name": "fireball"
        },
        {
            "name": "Goblin Scout",
            "health": 6,
            "strength": 5,
            "intellect": 2,
            "luck": 2,
            "attack_name": "Club Bash"
        }]

    medium_enemies = [
        {
            "name": "Dire Wolf",
            "health": 15,
            "strength": 5,
            "intellect": 3,
            "luck": 6,
            "attack_name": "Wolf Bite"
        },
        {
            "name": "Lesser Demon",
            "health": 10,
            "strength": 4,
            "intellect": 7,
            "luck": 2,
            "attack_name": "Soul Decay Wave"
        }]

    large_enemies = [
                    {
        "name": "Cave Troll",
        "health": 30,
        "strength": 10,
        "intellect": 1,
        "luck": 2,
        "attack_name": "Club Smash"
    },
    {
        "name": "Stunted Ice Drake",
        "health": 25,
        "strength": 9,
        "intellect": 7,
        "luck": 8,
        "attack_name": "Blizzard Breath"
    } ]
    @staticmethod
    def enemy_encounter(player_instance):
        enemy_chance = random.randint(0,4)
        if enemy_chance == 6:
            print("WTF, You're not supposed to see this, some kind of Cosmic bit flip happened")

        elif enemy_chance == 0 or enemy_chance == 1:
            enemy_attributes = random.choice(__class__.small_enemies)
            
        elif enemy_chance == 2 or enemy_chance == 3:
            enemy_attributes = random.choice(__class__.medium_enemies)

        elif enemy_chance == 4:
            enemy_attributes = random.choice(__class__.large_enemies)

        enemy_instance = Enemy(
    name=enemy_attributes['name'],
    health=enemy_attributes['health'],
    strength=enemy_attributes['strength'],
    intellect=enemy_attributes['intellect'],
    luck=enemy_attributes['luck'],
    attack_name=enemy_attributes['attack_name']
)
        Display.encounter_message(enemy_instance.name)
        player_action = Interaction.encounter_enemy()
        match player_action:
            case "ATTACK":
                    Combat.battle(player_instance, enemy_instance)
            case "FLEE":
                if player_instance.luck >= random.randint(4,15):
                    Display.flee_success_message(enemy_instance.name)
                else:
                    Display.flee_failure_message(enemy_instance.name)
                    Combat.battle(player_instance, enemy_instance)



