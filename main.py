import pickle
from actors.actor_player import Player
from message.message import Message
from interaction.interaction import Interaction
from encounters.encounter import check_for_encounter
from welcome import welcome, player_start, get_start_type

welcome()
if Interaction.global_game_mode == "MANUAL":
    match get_start_type():
        case "LOAD":
            with open('savegame.rpygs', 'rb') as file:
                # Write some text to the file.
                player_instance = pickle.load(file) #(maybe some way to make that safer or add a checksum or hash could be fun)
                print(f"Successfully Loaded Save Game for: {player_instance.name}")
        case "NEW":
            player_name = player_start()
            player_instance = Player(name=player_name)
else:
    player_instance = Player(name="The Protagonist")



while player_instance.progress < 100:
    player_instance.progress += 1
    Message.player_progress_message(player_instance)
    check_for_encounter(player_instance)
    if player_instance.health == 0:
        print(f"{player_instance.name} has fallen in combat after {player_instance.progress * 10} miles" , end='\n\n')
        break




Message.post_game_recap(player_instance)


### TODO expand merchant system

### TODO expand enemy system
    ### TODO Multi Enemy Encouters

### TODO add Defend & Dodge Options to combat

### Add interaction to rest encounters

### Remove direct prints from rest and mystery encounters

### Template and Json-ize rest and mystery encounters
### Move display functions into smaller sub classes (like encounters)
### Move interaction functions into smaller sub classes

### IDEA Centralize json stores in story directory?


### Gameplan: The Party Update
# no more followers big sad

# each game can have from 1-3 party memebers

# can be warrior, mage, rogue, (1 of each or 2 + 1 or 3 + 0)

# combat flow will be an option to pick a party memeber then their action.

# enemies will attack in packs, this will allow for bosses to be powered up more

# all exposed health & Damage values will be scaled by 10x, base player health will be 100 + 5 for each STR point

# add randomness to damage values

# Attack power will be set re balanced to be better based on attributes.

#classes will be balanceed with a min of 5 in the chosen attribute but an max of 5 in the other
# rogue's can will have 5 in AGL, but the other values are uncapped

#attack order will be each party member, then each enemy
#create extra comabt option, defend, protect, evade for each specilication

## add damage type (pysical, magic,)
## mages have resist to magic but weak to pysical, vise versa for warrior, rogue is balanced and has their resistances set based on attributes

## update welcome.py to ask for party size, auto will do 3 always

#strech goal: add AOE attack that can hit all enemy or player instances
#strach goal: add leveling system based on battle actions
#strech goal: add 2nd attack type for each class with new names (need to move to json)
