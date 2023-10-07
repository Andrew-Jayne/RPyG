import random
from player import Player
from encounters import Encounters

step = 0

strength = random.randint(1,10)
intellect = random.randint(1,10)
gold = strength * 25
potions = int(intellect / 2) 


# Initialize Player
player_params = {
    "name": "The Protagonist",
    "health": 50,
    "strength": 10,#strength,
    "intellect": 10,#intellect,
    "gold": gold,
    "potions": potions
}

player_instance = Player(**player_params)

print(f"Player Int: {player_instance.intellect}")
print(f"Player Str: {player_instance.strength}")

while step < 100:
    step += 1
    print(step)
    Encounters.check_for_encounter(player_instance=player_instance,step=step)
    if player_instance.health == 0:
        print(f"{player_instance.name} has fallen in combat after {step * 10} miles" , end='\n\n')
        break


print(f"Player Int: {player_instance.intellect}")
print(f"Player Str: {player_instance.strength}")
print(f"Player Gold: {player_instance.gold}")
print(f"Player Potions: {player_instance.potions}")
print(f"Player Attack: {player_instance.set_player_attack_name()}")
print(f"Player Skill: {player_instance._get_player_skill()}")

## TODO Improve balance

## TODO Sweep for jank