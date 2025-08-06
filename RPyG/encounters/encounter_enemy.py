import random

# Only for Type Checking / Hinting
from RPyG.actors import PlayerParty
from RPyG.combat import battle
from RPyG.content import ContentLibrary
from RPyG.content.enemy_library import EnemySet
from RPyG.interaction.interaction import Interaction
from RPyG.message.message import Message
from RPyG.utilites import ensure_type


def enemy_encounter(player_party_instance: PlayerParty) -> None:
    ensure_type(player_party_instance, PlayerParty, "player_party_instance")
    enemy_set: EnemySet
    enemy_count: int
    content_library: ContentLibrary = ContentLibrary.get_library()

    match random.randint(0, 4):
        case 0 | 1:
            enemy_set = random.choice(content_library.small_enemies)
            enemy_count = len(player_party_instance.members) + random.randint(-1, 3)
        case 2 | 3:
            enemy_set = random.choice(content_library.medium_enemies)
            enemy_count = len(player_party_instance.members) + random.randint(-2, 2)
        case 4:
            enemy_set = random.choice(content_library.large_enemies)
            enemy_count = len(player_party_instance.members) + random.randint(-2, 1)
        case _:
            raise ValueError(
                "Comsic Bit Flip has occured and `random.randint(0, 4)` has returned something it shouldn't"
            )

    # Set Enemy Count
    if enemy_count <= 0:
        enemy_count = 1

    enemy_party = EnemySet.generate_enemy_party(enemy_set, enemy_count)

    Message.encounter_message(enemy_party.name)
    match Interaction.encounter_enemy():
        case "BATTLE":
            battle(player_party_instance, enemy_party)
        case "FLEE":
            for player_instance in player_party_instance.members:
                if player_instance.luck >= random.randint(4, 15):
                    Message.flee_success_message(player_instance.name, enemy_party.name)
                else:
                    Message.flee_failure_message(player_instance.name, enemy_party.name)
                    battle(player_party_instance, enemy_party)
                    break
