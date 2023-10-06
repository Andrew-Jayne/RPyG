import random
from player import Player
from encounters import Encounters

step = 0

#Initialize Player
player_instance = Player("Protagonist", 20)


while step < 100:
    step += 1
    print(step)
    Encounters.check_for_encounter(player_instance)
    if player_instance.health == 0:
        print(f"{player_instance.name} has fallen in combat after {step * 10} miles")
        break
    




### Todo
### Upgrade encounter system, to have more than 1 positive and 1 negative encounter

### positive [Inn +5 HP, Tavern +3 HP]
### Negative [Monster -5 HP, Bandit -3 HP]

### Add Magicka & Stamina (no function just put them there)

### add basic attributes (Str, Int, Agl) (No function yet Mostly a placeholder / prep for actor class)

### Inventory System Same idea as attributes, no function but it's there (Gold, Health Potions)

## Inv and Attrib would be classes nested into the player class (eh... we can just have them be part of the class directly for now)

