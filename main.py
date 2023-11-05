from actor_player import Player
from display import Display
from encounters import check_for_encounter
from welcome import welcome, player_start

player_instance = []
welcome()

player_name = player_start()

player_instance = Player(name=player_name)


while player_instance.progress < 100:
    player_instance.progress += 1
    Display.player_progress_message(player_instance)
    check_for_encounter(player_instance)
    if player_instance.health == 0:
        print(f"{player_instance.name} has fallen in combat after {player_instance.progress * 10} miles" , end='\n\n')
        break




# Post Game Report
print(f"Player Name: {player_instance.name}")
print(f"Player Base Health: {player_instance.base_health}")
print(f"Player Int: {player_instance.intellect}")
print(f"Player Str: {player_instance.strength}")
print(f"Player Lck: {player_instance.luck}")
print(f"Player Gold: {player_instance.gold}")
print(f"Player Potions: {player_instance.potions}")
print(f"Player Attack: {player_instance.attack_name}")
print(f"Player Skill: {player_instance._get_skill()}")

print(f"Player Has Follower?: {player_instance.has_follower}")
if player_instance.has_follower == True:
    print(f"Player Follower is {player_instance.follower_instance.__dict__}")


### TODO expand merchant system

### TODO expand enemy system
    ### TODO Multi Enemy Encouters

