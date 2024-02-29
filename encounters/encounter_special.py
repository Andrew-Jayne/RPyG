import random
import json
import copy
from gameState.file import save_game
from interaction.interaction import Interaction
from message.message import Message
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
        Message.special_encounter_message(player_party_instance.progress, player_party_instance.name,"messages")
        Interaction.embark()

    @staticmethod
    def friendly_keep_visit(player_party_instance:PlayerParty) -> None:
        if not isinstance(player_party_instance, PlayerParty):
            raise ValueError("The 'player_party_instance' parameter must be of type PlayerParty. Received type: {}".format(type(player_party_instance).__name__))

        keep_visit_message = f"{player_party_instance.name} is welcomed at the Open Hall by King Stallman"
        Message.display_message(keep_visit_message, 1)
        Message.special_encounter_message(player_party_instance.progress, player_party_instance.name,"messages")
        Interaction.accept_quest()
        for member_instance in player_party_instance.members:
            member_instance.heal(300)
            member_instance.gain_potion(9)

        keep_depart_message = f"{player_party_instance.name} is are fully rested and have a full stock of potions"
        Message.display_message(keep_depart_message, 2)


    @staticmethod
    def midway_boss(player_party_instance:PlayerParty) -> None:
        if not isinstance(player_party_instance, PlayerParty):
            raise ValueError("The 'player_party_instance' parameter must be of type PlayerParty. Received type: {}".format(type(player_party_instance).__name__))

        enemy_instance = __class__._get_special_enemy('midway_boss')
        Message.special_encounter_message(player_party_instance.progress, player_party_instance.name,"messages")
        enemy_party = EnemyParty(enemy_instance.name, [enemy_instance])
        Combat.battle(player_party_instance, enemy_party)
        if len(player_party_instance.members) != 0:
            Message.special_encounter_message(player_party_instance.progress, player_party_instance.name,"success_messages")
        else:
            Message.special_encounter_message(player_party_instance.progress, player_party_instance.name,"failure_messages")

    ## holy Fucking Yikes....
    @staticmethod
    def enemy_keep_visit(player_party_instance:PlayerParty) -> None:
        if not isinstance(player_party_instance, PlayerParty):
            raise ValueError("The 'player_party_instance' parameter must be of type PlayerParty. Received type: {}".format(type(player_party_instance).__name__))
        sub_step = 0
        while sub_step < 10:
            sub_step += 1
            Message.display_message(sub_step, 1)
            dungeon_chance = random.randint(0,5)
            match dungeon_chance:
                case 0:
                    Message.display_message("Your Party finds a Store Room with some food & potions", 1)
                    for member_instance in player_party_instance.members:
                        member_instance.gain_potion(2)
                        member_instance.heal(20)
                case 1:
                    sub_step += 2
                    Message.display_message("Your Party finds a Secret Passage!", 1)
                case 4:
                    enemy_instance = __class__._get_special_enemy('keep_minion') ## Need to move this to a Party
                    Message.display_message(f"Your Party encounter a group of {enemy_instance.name}s!", 1)
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
            Message.display_message("At the end of the Keep Your Party encounters Algolon's Arch Mage!", 1)
            enemy_instance = __class__._get_special_enemy('keep_master')
            enemy_party = EnemyParty(enemy_instance.name, [enemy_instance])
            Combat.battle(player_party_instance, enemy_party)
            if len(player_party_instance.members) != 0:
                Message.special_encounter_message(player_party_instance.progress, player_party_instance.name,"success_messages")
            else:
                Message.special_encounter_message(player_party_instance.progress, player_party_instance.name,"failure_messages")

    @staticmethod
    def penultimate_boss(player_party_instance:PlayerParty) -> None:
        if not isinstance(player_party_instance, PlayerParty):
            raise ValueError("The 'player_party_instance' parameter must be of type PlayerParty. Received type: {}".format(type(player_party_instance).__name__))

        enemy_instance = __class__._get_special_enemy('penultimate_boss')
        Message.display_message(f"Your Party Battles {enemy_instance.name}!", 1)
        enemy_party = EnemyParty(enemy_instance.name, [enemy_instance])
        Combat.battle(player_party_instance, enemy_party)
        if len(player_party_instance.members) != 0:
            Message.special_encounter_message(player_party_instance.progress, player_party_instance.name,"success_messages")
        else:
            Message.special_encounter_message(player_party_instance.progress, player_party_instance.name,"failure_messages")

    @staticmethod
    def final_boss(player_party_instance:PlayerParty) -> None:
        if not isinstance(player_party_instance, PlayerParty):
            raise ValueError("The 'player_party_instance' parameter must be of type PlayerParty. Received type: {}".format(type(player_party_instance).__name__))

        enemy_instance = __class__._get_special_enemy('ultimate_boss')
        Message.display_message(f"Your Party must now battle {enemy_instance.name}!", 1)
        enemy_party = EnemyParty(enemy_instance.name,[enemy_instance])
        Combat.battle(player_party_instance, enemy_party)
        if len(player_party_instance.members) != 0:
            Message.special_encounter_message(player_party_instance.progress, player_party_instance.name,"success_messages")
            end_game_message = f"""
Fortranus the Ancient One has been Vanquished at the hands of {player_party_instance.name}


Your adventure has been completed, you may start a new adventure if you so choose
"""

            __class__.display_message(end_game_message, 2)

            if Interaction.global_game_mode == "MANUAL":
                save_game(player_party_instance)
            else:
                Message.special_encounter_message(player_party_instance.progress, player_party_instance.name,"failure_messages")
            
        
    ## Hidden Methods
    def _get_special_enemy(enemy_identifier) -> object:
        with open('encounters/enemies_special.json', 'r') as file:
            enemies_list = json.load(file)
        enemy_attributes = enemies_list[enemy_identifier]
        
        return Enemy(enemy_attributes)