import random
from player import Player
from encounters import Encounters

step = 0

strength = random.randint(1,10)
intellect = random.randint(1,10)
gold = intellect * 25
potions = int(strength / 2) 

# Initialize Player
player_params = {
    "name": "Protagonist",
    "health": 20,
    "strength": strength,
    "intellect": intellect,
    "gold": gold,
    "potions": potions
}

player_instance = Player(**player_params)

while step < 100:
    step += 1
    print(step)
    Encounters.check_for_encounter(player_instance)
    if player_instance.health == 0:
        print(f"{player_instance.name} has fallen in combat after {step * 10} miles")
        break


print(f"Player Int: {player_instance.intellect}")
print(f"Player Str: {player_instance.strength}")
print(f"Player Gold: {player_instance.gold}")
print(f"Player Potions: {player_instance.potions}")
