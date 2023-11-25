import random
import json
from actors.actor_enemy import Enemy
from combat import Combat
from display.display import Display
from interaction.interaction import Interaction

class EnemyEncounters():

    @staticmethod
    def enemy_encounter(player_instance):
        enemy_chance = random.randint(0,4)
        with open('encounters/enemies_common.json', 'r') as enemies_file:
            enemies_lists = json.load(enemies_file)
        if enemy_chance == 6:
            print("WTF, You're not supposed to see this, some kind of Cosmic bit flip happened")

        elif enemy_chance == 0 or enemy_chance == 1:
            enemy_attributes = random.choice(enemies_lists['small_enemies'])
            
        elif enemy_chance == 2 or enemy_chance == 3:
            enemy_attributes = random.choice(enemies_lists['medium_enemies'])

        elif enemy_chance == 4:
            enemy_attributes = random.choice(enemies_lists['large_enemies'])

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
            case "BATTLE":
                    Combat.battle(player_instance, enemy_instance)
            case "FLEE":
                if player_instance.luck >= random.randint(4,15):
                    Display.flee_success_message(enemy_instance.name)
                else:
                    Display.flee_failure_message(enemy_instance.name)
                    Combat.battle(player_instance, enemy_instance)



