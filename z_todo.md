# RoadMap

# Combat Updates
Flesh out combat system with blocking, damage types (melee, magic, frost, fire), add unique attacks to players and enemies
add persistent effects, allowing for lingering damage, healing spells, defense buffs

[] add damage type (Magic, Melee) + Resistances based on Specalization


# General Updates
## Leveling & Purchasing
Players become stronger as they progress and can gain temp and perm buffs from items, either found or bought
[] expand merchant system
[] add leveling system based on battle actions 

Party can find or buy relics which boost stats of the whole party, but can also be stolen 


# Encounter updates

### Travel Encounter
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

Would keep there from being major immersion violations due to RNG

### Mini Dungeons as Objects & encounter Expansions 
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