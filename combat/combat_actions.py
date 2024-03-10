import random
from gameState.file import save_game
from message.message import Message
from interaction.interaction import Interaction


# Only for Type Checking
from actors.actor_party import PlayerParty
from actors.actor_party import Party
from actors.actor_combatant import Combatant
from actors.actor_playable import PlayableActor
from actors.actor_enemy import Enemy

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

def react(combatant_instance:Combatant) -> bool:
    if not isinstance(combatant_instance, Combatant):
        raise ValueError("The 'combatant_instance' parameter must be of type Combatant. Received type: {}".format(type(combatant_instance).__name__))
    if isinstance(combatant_instance, PlayableActor):
        match combatant_instance.specialization:
            case 'WARRIOR':
                react_result = random.randint(1,30) <= (combatant_instance.luck + combatant_instance.strength)
            case 'MAGE':
                react_result = random.randint(1,30) <= (combatant_instance.luck + combatant_instance.intellect)
            case 'ROGUE':
                react_result = random.randint(1,30) <= (combatant_instance.luck + combatant_instance.agility)
    else:
        react_result = random.randint(1,30) <= (combatant_instance.luck + combatant_instance.agility)
    return react_result

def dismember_attack(attacker_instance:Combatant, target_instance:Combatant) -> None:
    if not isinstance(attacker_instance, Combatant):
        raise ValueError("The 'attacker_instance' parameter must be of type Combatant. Received type: {}".format(type(attacker_instance).__name__))
    if not isinstance(target_instance, Combatant):
        raise ValueError("The 'target_instance' parameter must be of type Combatant. Received type: {}".format(type(target_instance).__name__))
    
    
    if random.randint(0,99) in [0,1,2]:
        if isinstance(target_instance, Enemy) and target_instance.is_special == False:
            decapitate_message = f"{attacker_instance.name} decapitates  {target_instance.name} killing them instantly"
            Message.display_message(decapitate_message, 1)
            target_instance.health = 0

    damage_variation = int(attacker_instance.attack_power * 0.1)
    final_damage = attacker_instance.attack_power + random.randint(-damage_variation,damage_variation)
    attack_damage = int(final_damage * 0.25)
    dismember_message = f"""
{attacker_instance.name} dismembers {target_instance.name} inflicting {attack_damage} damage
{target_instance.name}'s attack power has been reduced by 25%
"""
    Message.display_message(dismember_message, 2)
    target_instance.dismember()
    target_instance.damage(attack_damage)

def aoe_attack(attacker_instance:Combatant, target_party_instance:Party) -> None:
    if not isinstance(attacker_instance, Combatant):
        raise ValueError("The 'attacker_instance' parameter must be of type Combatant. Received type: {}".format(type(attacker_instance).__name__))
    if not isinstance(target_party_instance, Party):
        raise ValueError("The 'target_party_instance' parameter must be of type Party. Received type: {}".format(type(target_party_instance).__name__))
    
    #set damage
    damage_variation = int(attacker_instance.attack_power * 0.1)
    final_damage = attacker_instance.attack_power + random.randint(-damage_variation,damage_variation)
    attack_damage = int(final_damage / len(target_party_instance.members))

    aoe_attack_message = f"{attacker_instance.name} attacks with {attacker_instance.special_attack_name} dealing {attack_damage} damage to all enemies"
    Message.display_message(aoe_attack_message, 1)
    for target_instance in target_party_instance.members:
        target_instance.damage(attack_damage)
    
    if attacker_instance.intellect <= random.randint(0,12):
        self_damage_amount = int(final_damage * 0.125)
        attacker_instance.damage(self_damage_amount)
        overwhelm_message = f"{attacker_instance.name} is overwhelmed by the power of {attacker_instance.special_attack_name} and takes {self_damage_amount} damage"
        Message.display_message(overwhelm_message, 1)

def double_attack(attacker_instance:Combatant, target_party_instance:Party) -> None:
    if not isinstance(attacker_instance, Combatant):
        raise ValueError("The 'attacker_instance' parameter must be of type Combatant. Received type: {}".format(type(attacker_instance).__name__))
    if not isinstance(target_party_instance, Party):
        raise ValueError("The 'target_party_instance' parameter must be of type Party. Received type: {}".format(type(target_party_instance).__name__))
    
    #set damage
    damage_variation = int(attacker_instance.attack_power * 0.1)
    final_damage = attacker_instance.attack_power + random.randint(-damage_variation,damage_variation)
    
    # set primary target
    primary_target_index = int(Interaction.choose_combat_target(target_party_instance))
    primary_instance = target_party_instance.members[primary_target_index]

    # set secondary target
    secondary_target_index = int(Interaction.choose_combat_target(target_party_instance))
    secondary_instance = target_party_instance.members[secondary_target_index]

    # exec damage
    primary_instance.damage(final_damage)
    Message.actor_attack_message(attacker_instance, final_damage)
    if primary_instance.health == 0:
        Message.defeated_message(primary_instance.name)
        target_party_instance.lose_member(primary_instance)

    secondary_instance.damage(int(final_damage * 0.5))
    Message.actor_attack_message(attacker_instance, int(final_damage * 0.5))
    if secondary_instance.health == 0:
        Message.defeated_message(secondary_instance.name)
        target_party_instance.lose_member(secondary_instance)

    # luck + agl in 25 to get caught and take 50% target damage from target 2
    if (attacker_instance.luck + attacker_instance.agility) < random.randint(0,25):
        attacker_instance.damage(int(secondary_instance.attack_power * 0.5))
        caught_attack_message = f"{attacker_instance.name} fails fails do evade an attack from {secondary_instance.name} and takes {int(secondary_instance.attack_power * 0.5)} damage"
        Message.display_message(caught_attack_message, 2)


def special_attack(attacker_instance:Combatant, target_party_instance:Party) -> None:
    if not isinstance(attacker_instance, Combatant):
        raise ValueError("The 'attacker_instance' parameter must be of type Combatant. Received type: {}".format(type(attacker_instance).__name__))
    if not isinstance(target_party_instance, Party):
        raise ValueError("The 'target_party_instance' parameter must be of type Party. Received type: {}".format(type(target_party_instance).__name__))
    
    if isinstance(attacker_instance, PlayableActor):
        match attacker_instance.specialization:
            case 'WARRIOR':
                target_index = int(Interaction.choose_combat_target(target_party_instance))
                target_instance = target_party_instance.members[target_index]
                if target_instance.is_dismembered == True:
                    dumb_check = 0 
                    while target_instance.is_dismembered == True:
                        dumb_check += 1
                        ## message that enemy has been dismembered
                        target_index = int(Interaction.choose_combat_target(target_party_instance))
                        target_instance = target_party_instance.members[target_index]
                        if dumb_check > 10:
                            ## dumb message
                            attack(attacker_instance, target_party_instance.members[0])
                        
                dismember_attack(attacker_instance=attacker_instance, target_instance=target_instance)
            case 'MAGE':
                aoe_attack(attacker_instance,target_party_instance)
            case 'ROGUE':
                double_attack(attacker_instance,target_party_instance)
    else:
        pass

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