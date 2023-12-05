import random

def mystery_encounter(party_instance):
    print("You Encounter A Strange Figure!")
    mystery_chance = random.randint(0,1)
    if mystery_chance == 0:
        print("The Figure heals you and vanishes into the darkness!")
        for member_instance in party_instance.members:
            member_instance.heal(3)
            print(f"Your Health is now {member_instance.health}") 
    else:
        print("The Figure blasts you with an Arcane Bolt and vanishes into a Flash of Light!", end="\n\n")
        for member_instance in party_instance.members:
            member_instance.damage(3)
            print(f"Your Health is now {member_instance.health}") 