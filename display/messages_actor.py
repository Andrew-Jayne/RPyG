## Generic Actor Messages
import time
from interaction.interaction import Interaction
from actors.actor_follower import Follower  


def encounter_message(actor_name):
    print(f"You encounter a {actor_name}!", end="\n\n")


def defeated_message(actor_name):
    print(f"{actor_name} has been defeated" , end='\n\n')


def actor_attack_message(actor_instance):
    if Interaction.global_game_mode != "AUTO" and isinstance(actor_instance, Follower) != True:
        time.sleep(2)
    print(f"{actor_instance.name} attacks with {actor_instance.attack_name} inflicting {actor_instance.attack_power} damage", end="\n\n")


def actor_critical_attack_message(actor_instance):
    if Interaction.global_game_mode != "AUTO" and isinstance(actor_instance, Follower) != True:
        time.sleep(2)
    print(f"{actor_instance.name} attacks with {actor_instance.attack_name} inflicting {actor_instance.attack_power * 2} damage")
    print(f"{actor_instance.name} got a critical hit!!", end="\n\n")



def actor_health_message(actor_instance):
    print(f"{actor_instance.name} has {actor_instance.health} Health remaining", end="\n\n")