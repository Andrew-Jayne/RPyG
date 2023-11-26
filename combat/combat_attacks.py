import random
from message.message import Message

def check_for_critical(combatant_instance):
    crit_check = random.randint(1,100)
    if crit_check <= combatant_instance.luck:
        return True
    else:
        return False


def attack(attacker_instance, target_instance):
    if check_for_critical(attacker_instance) == True:
        Message.actor_attack_message(attacker_instance)
        target_instance.damage(attacker_instance.attack_power * 2)
    else:
        Message.actor_attack_message(attacker_instance)
        target_instance.damage(attacker_instance.attack_power)