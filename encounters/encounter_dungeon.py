import random
import time

from actors.actor_enemy import Enemy

# Just for Type Checking
from actors.actor_party import EnemyParty, PlayerParty
from combat.combat import Combat
import config
from encounters.encounter_enemy import generate_enemy_party
from interaction.interaction import Interaction
from message.message import Message
from utilites.utilities import ensure_type


class Dungeon:
    def __init__(self, dungeon_attributes: dict) -> None:
        self.name = dungeon_attributes["name"]
        self.messages = dict(dungeon_attributes["messages"])
        self.length = dungeon_attributes["length"]
        self.enemies = dungeon_attributes["enemies"]
        self.boss = dungeon_attributes["boss"]

    def travese_dungeon(self, player_party_instance: PlayerParty) -> bool:
        ensure_type(player_party_instance, PlayerParty, "player_party_instance")
        dungeon_progress = 0
        Message.display_message(self.messages["start_message"], 2)

        while dungeon_progress < self.length:
            dungeon_progress += 1
            if config.GLOBAL_GAME_MODE == "MANUAL":
                time.sleep(2)
            encouter_chance = random.randint(0, 5)
            match encouter_chance:
                case 0:
                    Message.display_message(self.messages["heal_room_message"], 1)
                    for member_instance in player_party_instance.members:
                        member_instance.gain_potion(2)
                        member_instance.heal(20)
                case 1:
                    dungeon_progress += 2
                    Message.display_message(self.messages["shortcut_message"], 1)
                case 4:
                    enemy_count = int(
                        len(player_party_instance.members) + random.randint(-2, 2)
                    )
                    if enemy_count == 0:
                        enemy_count = 1
                    chosen_enemy = random.choice(self.enemies)
                    enemy_party = generate_enemy_party(chosen_enemy, enemy_count)
                    Message.encounter_message(enemy_party.name)
                    Combat.battle(player_party_instance, enemy_party)
                    if len(player_party_instance.members) == 0:
                        return False
                case _:
                    Message.empty_travel_message(1)

        if len(player_party_instance.members) != 0:
            Message.display_message(
                "At the end of the Keep Your Party encounters Algolon's Arch Mage!", 1
            )
            enemy_instance = Enemy(self.boss)
            enemy_party = EnemyParty(enemy_instance.name, [enemy_instance])
            Combat.battle(player_party_instance, enemy_party)
            if len(player_party_instance.members) != 0:
                Message.special_encounter_message(
                    player_party_instance.progress,
                    player_party_instance.name,
                    "success_messages",
                )
                return True
            else:
                Message.special_encounter_message(
                    player_party_instance.progress,
                    player_party_instance.name,
                    "failure_messages",
                )
                return False
