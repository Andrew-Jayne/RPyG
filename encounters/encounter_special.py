import random
import json
import copy
from actors.actor_enemy import Enemy
from actors.actor_party import EnemyParty
from combat.combat import Combat
from message.message import Message

class SpecialEncounters():

    @staticmethod
    def friendly_keep_visit(party_instance:object) -> None:
        print("Your Party is welcomed to the Keep of Stallman")
        print("Your Party is are fully rested and have a full stock of potions", end="\n\n")
        for member_instance in party_instance.members:
            member_instance.heal(300)
            member_instance.gain_potion(9)

    @staticmethod
    def midway_boss(party_instance:object) -> None:
        enemy_instance = __class__._get_special_enemy('midway_boss')
        print(f"Your Party encounters {enemy_instance.name}!")
        enemy_party = EnemyParty(enemy_instance.name, [enemy_instance])
        Combat.battle(party_instance, enemy_party)

    @staticmethod
    def enemy_keep_visit(party_instance:object) -> None:
        print("Your Party must traverse Algolon's Keep!")
        sub_step = 0
        while sub_step < 10:
            sub_step += 1
            print(sub_step)
            dungeon_chance = random.randint(0,5)
            match dungeon_chance:
                case 0:
                    print("Your Party finds a Store Room with some food & potions")
                    for member_instance in party_instance.members:
                        member_instance.gain_potion(2)
                        member_instance.heal(20)
                case 1:
                    sub_step += 2
                    print("Your Party finds a Secret Passage!")
                case 4:
                    enemy_instance = __class__._get_special_enemy('keep_minion') ## Need to move this to a Party
                    print(f"Your Party encounter a group of {enemy_instance.name}s!")
                    enemy_count = int(len(party_instance.members) + random.randint(-2,2))
                    if enemy_count == 0:
                        enemy_count = 1

                    enemy_party_instances = []
                    for _ in range(0,enemy_count):
                        enemy_party_instances.append(copy.deepcopy(enemy_instance))
                    enemy_party = EnemyParty(f"group of {enemy_count} {enemy_instance.name}" ,enemy_party_instances)
                    Combat.battle(party_instance, enemy_party)
            if len(party_instance.members) == 0:
                break
        print("At the end of the Keep Your Party encounters Algolon's Arch Mage!")
        enemy_instance = __class__._get_special_enemy('keep_master')
        enemy_party = EnemyParty(enemy_instance.name, [enemy_instance])
        Combat.battle(party_instance, enemy_party)

    @staticmethod
    def penultimate_boss(party_instance:object) -> None:
        enemy_instance = __class__._get_special_enemy('penultimate_boss')
        print(f"Your Party Battles {enemy_instance.name}!")
        enemy_party = EnemyParty(enemy_instance.name, [enemy_instance])
        Combat.battle(party_instance, enemy_party)

    @staticmethod
    def final_boss(party_instance:object) -> None:
        enemy_instance = __class__._get_special_enemy('ultimate_boss')
        print(f"Your Party must now battle {enemy_instance.name}!")
        enemy_party = EnemyParty(enemy_instance.name,[enemy_instance])
        Combat.battle(party_instance, enemy_party)
        if len(party_instance.members) != 0:
            Message.end_game_message(party_instance)
        


    ## Hidden Methods
    def _get_special_enemy(enemy_identifier) -> object:
        with open('encounters/enemies_special.json', 'r') as file:
            enemies_list = json.load(file)
        enemy_attributes = enemies_list[enemy_identifier]
        
        return Enemy(enemy_attributes)