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
        the_player.damage(3)
        print(f"Your Health is now {the_player.health}")
        if the_player.health == 0:
            print(f"you have fallen in combat at step {step}")
            break
    elif encounter_check == 1:
        print("You Find an Inn and Rest")
        the_player.heal(5)
        print(f"Your Health is now {the_player.health}")
    else:
        print(step)