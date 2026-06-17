# fmt: off
welcome_message = """
             This game looks best with a width of at least 80.
            If the next line is split please widen your terminal.
----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----

"""

# Standard Attack
attack_string = "{source_actor_name} attacks with {attack_name} inflicting {magnitude} damage to {target_actor_name}"
critical_attack_string = "{source_actor_name} got a critical hit!"

# AOE Attack
aoe_attack_string = "{source_actor_name} attacks with {attack_name} dealing {per_target_damage} damage to all enemies"
aoe_critical_string = "{source_actor_name} dealt critical hits to all enemies!"
aoe_self_damage_string = "{source_actor_name} is overwhelmed by the power of {attack_name} and takes {self_damage_magnitude} damage"

# Double Attack
self_damage_str = "{source_actor_name} fails fails to evade an attack from {secondary_target_name} and takes {self_damage_magnitude} damage"

# Dismember Attack
decapitate_string = "{source_actor_name} decapitates {target_actor_name} killing them instantly"
dismember_string = "{source_actor_name} dismembers {target_actor_name}\n{target_actor_name}'s attack power has been reduced by 25%"
no_valid_targets_strings = "All avalible enemies have been dismembered, select a target for a normal attack"

# Actor Defeated
actor_defeated_string = "{actor_name} has been defeated"

# Health Update
health_remaining_string = "{actor_name} has {remaining_health} Health Remaining"

# Use Potion
drink_potion_string = "{actor_name} drinks a potion"
no_potions_string = "{actor_name} has no remaining potions!"
already_full_heal_string = "{actor_name} is already fully healed!"

# Use Gold
insufficient_gold_string = "{actor_name} has insufficient gold"
no_gold_string = "{actor_name} has no gold remaining"

# Enemy Encounter
enemy_encounter_string = "Your Party encounters a {enemy_party_name}!"

# Battle Start / End
battle_start_string = "The Battle Begins!"
battle_victory_string = "{enemy_party_name} has been defeated"

# Flee
flee_success_string = "{actor_name} has Successfully Escaped the {enemy_party_name}!"
flee_fail_string = "{actor_name} has Failed to Escape the {enemy_party_name}!"

# Merchant
merchant_menu_string = "{actor_name} has {potion_count} potions & {gold_count} gold"
merchant_buy_string = "{buyer_actor_name} purchases a potion. They now have {remaining_potions} potions & {remaining_gold} gold"
merchant_insufficient_string = "{buyer_actor_name} does not have enough Gold to purchase more potions"

# Travel
travel_distance_string = "After {distance} miles of travel"
