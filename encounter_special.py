import random
from actor_enemy import Enemy
from combat import Combat
from actor_follower import Follower

class SpecialEncounters():

    @staticmethod
    def friendly_keep_visit(player_instance):
        print("You are welcomed to the Keep of Stallman")
        print("You are fully rested and have a full stock of potions", end="\n\n")
        player_instance.heal(30)
        player_instance.potions = 9

    @staticmethod
    def midway_boss(player_instance):
        wizard = Enemy(name="Cobolus The Wizard",health=15, strength=4, intellect=8, luck=6, attack_name="Arcane Firestorm")
        print(f"You encounter {wizard.name}!")
        enemy_instance = wizard
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
                    player_instance.potions += 2
                    player_instance.heal(2)
                    print("You find a Store Room with some food & potions")
                case 1:
                    sub_step += 2
                    print("You find a Secret Passage!")
                case 4:
                    mage = Enemy(name="Acolyte of Algolon", health=8, strength=3, intellect=7, luck=6, attack_name="Arcane Bolt")
                    print(f"You encounter an {mage.name}!")
                    enemy_instance = mage
                    Combat.battle(player_instance, enemy_instance)
            if player_instance.health == 0:
                break
        print("At the end of the Keep you encounter Algolon's Arch Mage!")
        arch_mage = Enemy(name="Algolon's Arch Mage", health=20, strength=4, intellect=10, luck=6, attack_name="Arcane Lightning")
        enemy_instance = arch_mage
        Combat.battle(player_instance, enemy_instance)

    @staticmethod
    def penultimate_boss(player_instance):
        great_wizard = Enemy(name="The Great Wizard Algolon", health=25, strength=5, intellect=12, luck=6, attack_name="Cosmic Collision")
        print(f"You Battle {great_wizard.name}!")
        enemy_instance = great_wizard
        Combat.battle(player_instance, enemy_instance)

    @staticmethod
    def final_boss(player_instance):
        dragon = Enemy(name="Fortranus the Ancient One", health=40, strength=14, intellect=10, luck=6, attack_name="Dragon Fire")
        print(f"You battle must now battle {dragon.name}!")
        enemy_instance = dragon
        Combat.battle(player_instance, enemy_instance)


    ## Hidden Methods
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
            follower_name_type = random.choice(mage_names,warrior_name)

        ## Set Follower Attributes (luck is handled in the class and is random, Follower also has gold and Potions using the same logic as player)
        if follower_name_type == mage_names:
            follower_intellect = 5 + random.randint(1,4)
            follower_strength = 5
            print(f"Impressed by your intellect, a young mage joins you on your quest")
        elif follower_name_type == warrior_name:
            follower_intellect = 5
            follower_strength = 5 + random.randint(1,4)
            print(f"Impressed by your strength, a young warrior joins you on your quest")
        
        ### setup Follower instance

        player_follower = Follower(name=follower_name_type[name_choice], strength=follower_strength, intellect=follower_intellect)


        ## Add Follower to Player Instance
        player_instance.gain_follower(player_follower)