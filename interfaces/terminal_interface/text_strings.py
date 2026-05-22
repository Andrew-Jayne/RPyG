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
