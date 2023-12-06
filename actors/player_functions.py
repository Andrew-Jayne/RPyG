import random
from actors.actor_playable import PlayableActor

def generate_player_attributes(name:str, specialization:str):
    match specialization:
            case "WARRIOR":
                strength = random.randint(5,10)
                intellect = random.randint(1,5)
                agility = random.randint(4,8)
                luck = random.randint(1,10)
            case "MAGE":
                strength = random.randint(1,5)
                intellect = random.randint(5,10)
                agility = random.randint(4,8)
                luck = random.randint(1,10)
            case "ROGUE":
                strength = random.randint(4,8)
                intellect = random.randint(4,8)
                agility = random.randint(5,10)
                luck = random.randint(1,10)
            case _:
                print(f"Error Invalid Specialization {specialization}")
                exit()

    health = 100 + int((strength + intellect) * 10)
    gold = strength * 25
    potions = int(intellect / 2) 

    return {
    "name": name,
    "specialization": specialization,
    "strength": strength,
    "intellect": intellect,
    "agility": agility,
    "luck": luck,
    "health": health,
    "gold": gold,
    "potions": potions
    }


def generate_player_instance(member):
    party_member_attributes = generate_player_attributes(member.name, member.specialization)
    party_member_instance = PlayableActor(
        name=party_member_attributes["name"],
        specialization=party_member_attributes["specialization"],
        strength=party_member_attributes["strength"],
        intellect=party_member_attributes["intellect"],
        agility=-party_member_attributes["agility"],
        luck=party_member_attributes["luck"],
        health=party_member_attributes["health"],
        gold=party_member_attributes["gold"],
        potions=party_member_attributes["potions"])
    
    return party_member_instance