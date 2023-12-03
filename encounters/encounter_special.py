import random
import json
from actors.actor_enemy import Enemy
from combat.combat import Combat
from actors.actor_follower import Follower
from message.message import Message

class SpecialEncounters():

    @staticmethod
    def friendly_keep_visit(player_instance):
        print("You are welcomed to the Keep of Stallman")
        print("You are fully rested and have a full stock of potions", end="\n\n")
        player_instance.heal(30)
        player_instance.potions = 9

    @staticmethod
    def midway_boss(player_instance):
        enemy_instance = __class__._get_special_enemy('midway_boss')
        print(f"You encounter {enemy_instance.name}!")
        Combat.battle(player_instance, enemy_instance)
        if player_instance.strength >= 7 or player_instance.intellect >= 7:
            __class__._follower_joins(player_instance)

    @staticmethod
    def enemy_keep_visit(player_instance):
        print("You must traverse Algolon's Keep!")
        sub_step = 0
        while sub_step < 10:
            sub_step += 1
            print(sub_step)
            dungeon_chance = random.randint(0,5)
            match dungeon_chance:
                case 0:
                    print("You find a Store Room with some food & potions")
                    player_instance.potions += 2
                    player_instance.heal(2)
                case 1:
                    sub_step += 2
                    print("You find a Secret Passage!")
                case 4:
                    enemy_instance = __class__._get_special_enemy('keep_minion')
                    print(f"You encounter an {enemy_instance.name}!")
                    Combat.battle(player_instance, enemy_instance)
            if player_instance.health == 0:
                break
        print("At the end of the Keep you encounter Algolon's Arch Mage!")
        enemy_instance = __class__._get_special_enemy('keep_master')
        Combat.battle(player_instance, enemy_instance)

    @staticmethod
    def penultimate_boss(player_instance):
        enemy_instance = __class__._get_special_enemy('penultimate_boss')
        print(f"You Battle {enemy_instance.name}!")
        Combat.battle(player_instance, enemy_instance)

    @staticmethod
    def final_boss(player_instance):
        enemy_instance = __class__._get_special_enemy('ultimate_boss')
        print(f"You battle must now battle {enemy_instance.name}!")
        Combat.battle(player_instance, enemy_instance)
        if player_instance.health > 0:
            Message.end_game_message(player_instance)
        


    ## Hidden Methods
    def _get_special_enemy(enemy_indentiier):
        with open('encounters/enemies_special.json', 'r') as file:
            enemies_list = json.load(file)
        enemy_attributes = enemies_list[enemy_indentiier]
        special_enemy_instance = Enemy(
            name=enemy_attributes['name'],
            health=enemy_attributes['health'],
            strength=enemy_attributes['strength'],
            intellect=enemy_attributes['intellect'],
            agility=enemy_attributes['agility'],
            luck=enemy_attributes['luck'],
            attack_name=enemy_attributes['attack_name'])
        
        return special_enemy_instance

    def _follower_joins(player_instance):
        
        mage_names = ["Grace","Torvalds","Knuth"]
        warrior_name = ["Moore","Neumann","Kilby"]
        name_choice = random.randint(0,2)

        ## Determine Follower Type
        if player_instance.intellect >= 7 and player_instance.intellect > player_instance.strength:
            follower_name_type = mage_names
        elif player_instance.strength >= 7 and player_instance.strength > player_instance.intellect:
            follower_name_type = warrior_name
        elif player_instance.strength == player_instance.intellect:
            follower_name_type = random.choice([mage_names,warrior_name])

        ## Set Follower Attributes (luck is handled in the class and is random, Follower also has gold and Potions using the same logic as player)
        if follower_name_type == mage_names:
            follower_intellect = 5 + random.randint(1,4)
            follower_strength = 5
            print(f"Impressed by your intellect, a young mage joins you on your quest")
        elif follower_name_type == warrior_name:
            follower_intellect = 5
            follower_strength = 5 + random.randint(1,4)
            print(f"Impressed by your strength, a young warrior joins you on your quest")
        
        follower_agility = 3 + random.randint(1,6)
        
        ### setup Follower instance

        player_follower = Follower(name=follower_name_type[name_choice], strength=follower_strength, intellect=follower_intellect, agility=follower_agility)


        ## Add Follower to Player Instance
        player_instance.gain_follower(player_follower)