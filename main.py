import random
step = 0 
health = 20

while step < 100:
    step += 1
    encounter_check = random.randint(1,10)
    if encounter_check == 5:
        print("An Enemy was encountered!")
        health -= 3
        if health == 0:
            print(f"you have fallen in combat at step {step}")
            break
    elif encounter_check == 1:
        print("You Find an Inn and Rest")
        health += 5
    else:
        print(step)