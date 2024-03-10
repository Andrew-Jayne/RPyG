## Message Project:
[*] All print statments in all functions are shipped to the message class and handled there, even if it's just a dumb print the input str funciton, prep for curses down the road

## V2 Goals (The Party Update) (Done!)
[*] RPC for Mystery Encounters
[*] Merge Rest & Mystery Encounters
[*] Finish Merchant Interaction
[*] Polish Special Encounters 
[*] Remove all remaining "You" Messages
[*] Remove Follower
[*] Add Randomness to Damage
[*] Remove direct prints from rest and mystery encounters~
[*] Move special encounter to line up with new json fommating
[*] Sweep for junk funcitons &| bloat
[*] Add enemy AIs
[*] add multi action encounters (you rest for the night but are robbed in your sleep and lose all of your gold!)
[*] Find out how auto player can buy infinite potions at the shop?


# RoadMap

## Combat Update
Flesh out combat system with blocking, damage types (melee, magic, frost, fire), add unique attacks to players and enemies
add persistent effects, allowing for lingering damage, healing spells, defense buffs
[] add AOE attack that can hit all enemy or player instances 
[*] Add Defend, Evade, Elude for secondary combat action

[*] add 2nd attack type for each class with new names (DONE!)
[] add damage type (Magic, Melee) + Resistances based on Specalization

Updated combat Ideas: (DONE!)

Main Attack (stock, uses standard attack calc for each specalizaion, needs updated names to keep rouge from using fireball and mage from using dagger slash)
Special attack (AOE For Mages, Dismember for warriors, Poision Blade for Rogue)

AOE: Attack all targets with 3/4 attack power, deals 1/8 of damage to self based on int check (int/15)

Dismember: Deal 1/4 damage but reduce enemy attack by 25% (once per enemy) (5% chance to decapitate enemies that are not 'special' for instant kill)

Double Strike: Can attack twice in a single turn, 2nd attack deals 50% less damage (can hit the same enemy or 2 of them)


## Mini Dungeons as Objects & encounter Expansions 
Use this for cobolus' lair and algolon's fortress (midway_dungeon, enemy_fortress)

build mini dungeons as objects with custom actors, rewards, and routes
```json
mini_dungeon:{
    "enemy_list": [],
    "length" : 10,
    "final_boss": {},
    "reward":{}
}
```
Add negative progress encounter (you get lost a lose a days progress)
add shortcuts, with dynamic chances for enemy and rest encounters
optional mini dungeons
Move all json files to a story dir with support for multiple files in enemies_common, encounters_special etc, to make it easy to import or export custom event packs

## Leveling & Purchasing
Players become stronger as they progress and can gain temp and perm buffs from items, either found or bought
[] expand merchant system
[] add leveling system based on battle actions 

Party can find or buy relics which boost stats of the whole party, but can also be stolen 


## Encounter updates

It might make sense to integrate enemy encounters into the standard encounter system and make that more robust, add "ENEMY ENCOUNTER" to the encounter JSON system?
IDK may end up being too complex

New encounter type (TRAVEL)
given a prompt has a chance based on total STR, INT or AGL of the party to clear an obstacle and gain +3 progress or lose -2

you see a steep mountain pass that would save you 30 miles of travel do you think you are agile enough to traverse it? (if party total AGL is over 18 success)
S: you traverse the pass saving 30 miles of travel
F: you become lost in the mountains and must back track wasting 20 miles of travel

(rough concept but the idea is there) (Also needs check to make sure you don't skip a story event)


 ### Encounter Zones

Based on being in the 0-25, 26-50, 51-75 & 76-99 progress zones

there are differing pools of encounters (you should not find a big city a step 98 right before the final boss), can also change enemy pools (frost drakes in the mtns, dire wolves in the plains, cave trolls in the canyons)

would keep there from being major immersion violations due to RNG
