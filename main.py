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
    "name": "Protagonist",
    "health": 30,
    "strength": strength,
    "intellect": intellect,
    "gold": gold,
    "potions": potions,
    "attack" : "Default: you should not see this"
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
print(f"Player Mag: {player_instance.magicka}")
print(f"Player Stam: {player_instance.stamina}")
print(f"Player Gold: {player_instance.gold}")
print(f"Player Potions: {player_instance.potions}")

## TODO Add upgraded attacks for player with over 5 int and str, Arcane Strike (Str + Int * .75) for power so maxed out could do 15 damage

## TODO Improve balance

## TODO pass step thru to encounter and have special events at 25,50,75,100 steps

## TODO Sweep for jank