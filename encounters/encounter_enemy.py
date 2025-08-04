import random

# Only for Type Checking / Hinting
from actors import EnemyParty, PlayerParty
from actors.actor_enemy import Enemy
from combat import battle
from content.content import ENEMIES_STANDARD
from content.enemy_library import EnemySet
from interaction.interaction import Interaction
from message.message import Message
from utilites import ensure_type


def generate_enemy_party(enemy_set: EnemySet, enemy_count: int) -> EnemyParty:
    ensure_type(enemy_set, EnemySet, "enemy_party_attributes")
    ensure_type(enemy_count, int, "enemy_count")

    # Create Instances & Add to Instance List
    enemy_party_instances: list[Enemy] = []
    for _ in range(0, enemy_count):
        variant_lists: list[list[Enemy]] = [
            enemy_set.variant_lists.lesser_variants,
            enemy_set.variant_lists.common_variants,
            enemy_set.variant_lists.greater_variants,
        ]

        active_variant_list: list[Enemy] = random.choice(variant_lists)

        variant_choice: Enemy = random.choice(active_variant_list)

        enemy_party_instances.append(variant_choice)
    if enemy_count == 1:
        enemy_party_name = f"Lone {enemy_party_instances[0].name}"
    else:
        enemy_party_name = (
            f"{enemy_set.group_name} of {enemy_count} {enemy_set.pural_name}"
        )

    return EnemyParty(enemy_party_name, enemy_party_instances)


def enemy_encounter(player_party_instance: PlayerParty) -> None:
    ensure_type(player_party_instance, PlayerParty, "player_party_instance")
    enemy_set: EnemySet

    match random.randint(0, 4):
        case 0 | 1:
            enemy_set = random.choice(ENEMIES_STANDARD.small_enemies)
        case 2 | 3:
            enemy_set = random.choice(ENEMIES_STANDARD.medium_enemies)
        case 4:
            enemy_set = random.choice(ENEMIES_STANDARD.large_enemies)
        case _:
            raise ValueError(
                "Comsic Bit Flip, has occured and `random.randint(0, 4)` has returned something it shoudn't"
            )

    # Set Enemy Count
    enemy_count = len(player_party_instance.members) + random.randint(-2, 2)
    if enemy_count <= 0:
        enemy_count = 1

    enemy_party = generate_enemy_party(enemy_set, enemy_count)

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
