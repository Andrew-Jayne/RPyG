from player import Player
from encounters import Encounters
from welcome import welcome

step = 0

player_name = str(welcome())

player_instance = Player(name=player_name)

while step < 100:
    step += 1
    print(step)
    Encounters.check_for_encounter(player_instance=player_instance,step=step)
    if player_instance.health == 0:
        print(f"{player_instance.name} has fallen in combat after {step * 10} miles" , end='\n\n')
        break

print(f"Player Base Health: {player_instance.base_health}")
print(f"Player Int: {player_instance.intellect}")
print(f"Player Str: {player_instance.strength}")
print(f"Player Gold: {player_instance.gold}")
print(f"Player Potions: {player_instance.potions}")
print(f"Player Attack: {player_instance.attack_name}")
print(f"Player Skill: {player_instance._get_player_skill()}")



### TODO Welcome system, prep for interactive mode, lower(sysargv) == auto to set auto mode, if manual then pass that to interaction as class var (split fucntions on mode)

### TODO add follower concept (a young X is impress by Y and joins you in your jounnry (this will need some tweaking to combat system follower_attack))

### TODO expand merchant system

### TODO implement interactive play