import random
from gameState.file import save_game
from message.message import Message
from interaction.interaction import Interaction


# Only for Type Checking
from actors.actor_party import PlayerParty
from actors.actor_combatant import Combatant

def check_for_critical(combatant_instance:Combatant) -> bool:
    if not isinstance(combatant_instance, Combatant):
        raise ValueError("The 'combatant_instance' parameter must be of type Combatant. Received type: {}".format(type(combatant_instance).__name__))

    crit_check = random.randint(1,100)
    if crit_check <= (combatant_instance.luck + combatant_instance.agility):
        return True
    else:
        return False

def attack(attacker_instance:Combatant, target_instance:Combatant) -> None:
    if not isinstance(attacker_instance, Combatant):
        raise ValueError("The 'attacker_instance' parameter must be of type Combatant. Received type: {}".format(type(attacker_instance).__name__))
    if not isinstance(target_instance, Combatant):
        raise ValueError("The 'target_instance' parameter must be of type Combatant. Received type: {}".format(type(target_instance).__name__))

    damage_variation = int(attacker_instance.attack_power * 0.1)
    final_damage = attacker_instance.attack_power + random.randint(-damage_variation,damage_variation)

    if check_for_critical(attacker_instance) == True:
        Message.actor_critical_attack_message(attacker_instance,final_damage)
        target_instance.damage(final_damage * 2)
    else:
        Message.actor_attack_message(attacker_instance, final_damage)
        target_instance.damage(final_damage)

def evade(combatant_instance:Combatant) -> bool:
    if not isinstance(combatant_instance, Combatant):
        raise ValueError("The 'combatant_instance' parameter must be of type Combatant. Received type: {}".format(type(combatant_instance).__name__))
    evade_result = random.randint(1,30) <= (combatant_instance.luck + combatant_instance.agility)
    return evade_result

def post_battle(player_party_instance:PlayerParty) -> None:
    if not isinstance(player_party_instance, PlayerParty):
        raise ValueError("The 'player_party_instance' parameter must be of type PlayerParty. Received type: {}".format(type(player_party_instance).__name__))

    player_post_action = ""
    while player_post_action != "TRAVEL":
        player_post_action = Interaction.post_battle(player_party_instance)
        if player_post_action == "HEAL":
            for member_instance in player_party_instance.members:
                member_instance.use_potion()
        if player_post_action == "SAVE":
            save_game(player_party_instance)