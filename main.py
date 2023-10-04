import random
from player import Player

#Initialize Player
the_player = Player("Protagonist", 20)

step = 0 

while step < 100:
    step += 1
    encounter_check = random.randint(1,8)
    if encounter_check == 5:
        print("An Enemy was encountered!")
        the_player.damage(5)
        print(f"Your Health is now {the_player.health}")
        if the_player.health == 0:
            print(f"{the_player.name} has fallen in combat at step {step}")
            break
    elif encounter_check == 1:
        print("You Find an Inn and Rest")
        the_player.heal(5)
        print(f"Your Health is now {the_player.health}")
    else:
        print(step)


### Todo
### Upgrade encounter system, to have more than 1 positive and 1 negative encounter

### positive [Inn +5 HP, Tavern +3 HP]
### Negative [Monster -5 HP, Bandit -3 HP]

### Add Magicka & Stamina (no function just put them there)

### add basic attributes (Str, Int, Agl) (No function yet Mostly a placeholder / prep for actor class)

### Inventory System Same idea as attributes, no function but it's there (Gold, Health Potions)

## Inv and Attrib would be classes nested into the player class (eh... we can just have them be part of the class directly for now)

