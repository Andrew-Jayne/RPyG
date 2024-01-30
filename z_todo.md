## V2 Goals (The Party Update)
[*] RPC for Mystery Encounters
[*] Merge Rest & Mystery Encounters
[*] Finish Merchant Interaction
[] Polish Special Encounters 
[*] Remove all remaining "You" Messages
[*] Remove Follower
[*] Add Randomness to Damage
[*] Remove direct prints from rest and mystery encounters
[] Move special encounter to line up with new json fommating
[] Sweep for junk funcitons &| bloat
[*] Add enemy AIs
[*] add multi action encounters (you rest for the night but are robbed in your sleep and lose all of your gold!)


## RoadMap

# Combat Update
Flesh out combat system with blocking, damage types (melee, magic, frost, fire), add unique attacks to players and enemies
add persistent effects, allowing for lingering damage, healing spells, defense buffs
[] add AOE attack that can hit all enemy or player instances
[] Add Defend, Evade, Elude for secondary combat action
[] Specalization based Attack Names (3 grades)

[] add 2nd attack type for each class with new names
[] add damage type (Magic, Melee) + Resistances based on Specalization


Updated combat Idea:

Main Attack 
Special attack (AOE For Mages, Dismember for warriors, Poision Blade for Rogue)

AOE: Attack all targets with 3/4 attack power, deals 1/8 of damage to self

Dismember: Deal 1/4 damage but reduce enemy attack by 25% (once per enemy)

Poison Blade: Deal 1/2 damage but Emeny takes 1/4 damage per turn for the rest of the battle


# Mini Dungeons as Objects
build mini dungeons as objects with custom actors, rewards, and routes
```json
mini_dungeon:{
    "enemy_list": [],
    "length" : 10,
    "final_boss": {},
    "reward":{}
}
```

# Arch & Spec
take the current 3 specaliazations and make them archetypes, then within those options for 3 archetypes
palidin, barbarian, knight
Wizard, Battle Mage, Sorcerer
Assasin, Theif, ?

# Leveling & Purchasing
Players become stronger as they progress and can gain temp and perm buffs from items, either found or bought
[] expand merchant system
[] add leveling system based on battle actions