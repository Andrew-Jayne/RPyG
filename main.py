import random
from player import Player
from encounters import Encounters

step = 0

strength = random.randint(1,10)
intellect = random.randint(1,10)
gold = intellect * 25
potions = int(strength / 2) 



## this needs to be moved over to the player class or combat class
attack = None
if intellect >= 5 and strength >= 5:
    attack = "Arcane Strike"
elif strength <= 5 and intellect >= 5:
    attack = "Arcane Bolt"
elif strength <= 5 and intellect >= 5:
    attack = "Sword Thrust"
elif intellect <= 5 and strength <= 5:
    attack = "Rock Throw"
else:
    attack = "Generic Attack The Dev is Lazy:)"

# Initialize Player
player_params = {
    "name": "Protagonist",
    "health": 20,
    "strength": strength,
    "intellect": intellect,
    "gold": gold,
    "potions": potions,
    "attack" : attack
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
print(f"Player ATK: {player_instance.attack}")
print(f"Player Str: {player_instance.strength}")
print(f"Player Mag: {player_instance.magicka}")
print(f"Player Stam: {player_instance.stamina}")
print(f"Player Gold: {player_instance.gold}")
print(f"Player Potions: {player_instance.potions}")
