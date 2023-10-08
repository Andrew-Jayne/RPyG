from actor_player import Player
from encounters import check_for_encounter
from welcome import welcome, player_start

step = 0
player_instance_list = []
welcome()

player_name_list = player_start()

for count in range(0,len(player_name_list)):
    player_instance = Player(name=player_name_list[count])
    player_instance_list.append(player_instance)


while step < 100:
    step += 1
    print(step)
    check_for_encounter(player_instance=player_instance_list[0],step=step) ## [0] forces the 1st instance in the list will be removed when multi player is done
    if player_instance.health == 0:
        print(f"{player_instance_list[0].name} has fallen in combat after {step * 10} miles" , end='\n\n')
        break

for player_instance in player_instance_list:
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

## TODO MultiPlayer Mode... (with auto? somehow? IDK?) 
# This is going to be on hold until the enemy system is expanded dramatically because I don't want to make a enemy selector right now.
