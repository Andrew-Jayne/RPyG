import random
import json
import copy
import time
import textwrap
from interaction.interaction import Interaction
from actors.actor_enemy import Enemy
from actors.actor_party import EnemyParty
from combat.combat import Combat
from message.message import Message

# Just for Type Checking
from actors.actor_party import PlayerParty


class SpecialEncounters():
    @staticmethod
    def tavern_notice(player_party_instance:PlayerParty)-> None:
        if not isinstance(player_party_instance, PlayerParty):
            raise ValueError("The 'player_party_instance' parameter must be of type PlayerParty. Received type: {}".format(type(player_party_instance).__name__))
        __class__._display_special_encounter_message(player_party_instance.progress, player_party_instance.name,"messages")

    @staticmethod
    def friendly_keep_visit(player_party_instance:PlayerParty) -> None:
        if not isinstance(player_party_instance, PlayerParty):
            raise ValueError("The 'player_party_instance' parameter must be of type PlayerParty. Received type: {}".format(type(player_party_instance).__name__))

        print(f"{player_party_instance.name} is welcomed at the Open Hall by King Stallman")
        __class__._display_special_encounter_message(player_party_instance.progress, player_party_instance.name,"messages")
        for member_instance in player_party_instance.members:
            member_instance.heal(300)
            member_instance.gain_potion(9)
        print(f"{player_party_instance.name} is are fully rested and have a full stock of potions", end="\n\n")

    @staticmethod
    def midway_boss(player_party_instance:PlayerParty) -> None:
        if not isinstance(player_party_instance, PlayerParty):
            raise ValueError("The 'player_party_instance' parameter must be of type PlayerParty. Received type: {}".format(type(player_party_instance).__name__))

        enemy_instance = __class__._get_special_enemy('midway_boss')
        __class__._display_special_encounter_message(player_party_instance.progress, player_party_instance.name,"messages")
        enemy_party = EnemyParty(enemy_instance.name, [enemy_instance])
        Combat.battle(player_party_instance, enemy_party)
        if len(player_party_instance.members) != 0:
            __class__._display_special_encounter_message(player_party_instance.progress, player_party_instance.name,"success_messages")
        else:
            __class__._display_special_encounter_message(player_party_instance.progress, player_party_instance.name,"failure_messages")

    @staticmethod
    def enemy_keep_visit(player_party_instance:PlayerParty) -> None:
        if not isinstance(player_party_instance, PlayerParty):
            raise ValueError("The 'player_party_instance' parameter must be of type PlayerParty. Received type: {}".format(type(player_party_instance).__name__))
        sub_step = 0
        while sub_step < 10:
            sub_step += 1
            print(sub_step)
            dungeon_chance = random.randint(0,5)
            match dungeon_chance:
                case 0:
                    print("Your Party finds a Store Room with some food & potions")
                    for member_instance in player_party_instance.members:
                        member_instance.gain_potion(2)
                        member_instance.heal(20)
                case 1:
                    sub_step += 2
                    print("Your Party finds a Secret Passage!")
                case 4:
                    enemy_instance = __class__._get_special_enemy('keep_minion') ## Need to move this to a Party
                    print(f"Your Party encounter a group of {enemy_instance.name}s!")
                    enemy_count = int(len(player_party_instance.members) + random.randint(-2,2))
                    if enemy_count == 0:
                        enemy_count = 1

                    enemy_party_instances = []
                    for _ in range(0,enemy_count):
                        enemy_party_instances.append(copy.deepcopy(enemy_instance))
                    enemy_party = EnemyParty(f"group of {enemy_count} {enemy_instance.name}" ,enemy_party_instances)
                    Combat.battle(player_party_instance, enemy_party)
            if len(player_party_instance.members) == 0:
                break
        if len(player_party_instance.members) != 0:
            print("At the end of the Keep Your Party encounters Algolon's Arch Mage!")
            enemy_instance = __class__._get_special_enemy('keep_master')
            enemy_party = EnemyParty(enemy_instance.name, [enemy_instance])
            Combat.battle(player_party_instance, enemy_party)
            if len(player_party_instance.members) != 0:
                __class__._display_special_encounter_message(player_party_instance.progress, player_party_instance.name,"success_messages")
            else:
                __class__._display_special_encounter_message(player_party_instance.progress, player_party_instance.name,"failure_messages")

    @staticmethod
    def penultimate_boss(player_party_instance:PlayerParty) -> None:
        if not isinstance(player_party_instance, PlayerParty):
            raise ValueError("The 'player_party_instance' parameter must be of type PlayerParty. Received type: {}".format(type(player_party_instance).__name__))

        enemy_instance = __class__._get_special_enemy('penultimate_boss')
        print(f"Your Party Battles {enemy_instance.name}!")
        enemy_party = EnemyParty(enemy_instance.name, [enemy_instance])
        Combat.battle(player_party_instance, enemy_party)
        if len(player_party_instance.members) != 0:
            __class__._display_special_encounter_message(player_party_instance.progress, player_party_instance.name,"success_messages")
        else:
            __class__._display_special_encounter_message(player_party_instance.progress, player_party_instance.name,"failure_messages")

    @staticmethod
    def final_boss(player_party_instance:PlayerParty) -> None:
        if not isinstance(player_party_instance, PlayerParty):
            raise ValueError("The 'player_party_instance' parameter must be of type PlayerParty. Received type: {}".format(type(player_party_instance).__name__))

        enemy_instance = __class__._get_special_enemy('ultimate_boss')
        print(f"Your Party must now battle {enemy_instance.name}!")
        enemy_party = EnemyParty(enemy_instance.name,[enemy_instance])
        Combat.battle(player_party_instance, enemy_party)
        if len(player_party_instance.members) != 0:
            __class__._display_special_encounter_message(player_party_instance.progress, player_party_instance.name,"success_messages")
            Message.end_game_message(player_party_instance)
        else:
            __class__._display_special_encounter_message(player_party_instance.progress, player_party_instance.name,"failure_messages")
            
        


    ## Hidden Methods
    def _get_special_enemy(enemy_identifier) -> object:
        with open('encounters/enemies_special.json', 'r') as file:
            enemies_list = json.load(file)
        enemy_attributes = enemies_list[enemy_identifier]
        
        return Enemy(enemy_attributes)
    
    def _display_special_encounter_message(progress_value:int, party_name:str,message_type:str)-> None:
            if message_type not in ["messages","success_messages","failure_messages"]:
                raise ValueError('Message type must be one of ["messages","success_messages","failure_messages"]')
            with open('encounters/story_events.json') as file:
                story_events_list = json.load(file)


            all_events = story_events_list['progress_events']

            current_event = all_events[str(progress_value)]
            for message in current_event[message_type]:
                formatted_message = message.format(party_name=party_name)

                print(textwrap.fill(formatted_message, width=80), end="\n\n")
                if Interaction.global_game_mode == "MANUAL":
                    time.sleep(2)