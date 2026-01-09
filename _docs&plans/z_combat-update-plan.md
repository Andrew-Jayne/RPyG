Set 3 Archtypes for attack

Melee
Ranged
Magic


take existing specials and give enemies access to them

rework dodge and defend system so that it does not use a turn

Warrior and Rogue (need broader class name)

Melee & Ranged class attackers can dodge or defend on every attack (prim atter + luck for success)

Magic users must use a turn, but can use it to cast "elude" on any one in their party for the next turn

Magic users can also heal themselves or others without potions

Buff Magic Damange and AOE, Mage becomes glass cannon

Warrior becomes more of a tank (option for greatsword (boosted damage by 50% but a malus to defense of 50%), sword and shield (balanced), or spears and sheild [option for ranged attack + melee at a 25% cost to damage output])

Mixed Psysical attackers (like a rogue) can use both ranged and melee attacks, (bow, daggers, shortsword) and can mix attacks on double strike


Need to set the base 3 attack classes, and give all non magic users at least 1 ranged and 1 melee attack, and option for spell blade.


concept, dragons can use Magic damage (frost breath), or melee (claw attack) so they get both an AOE option and dismember (the bite off your fuckin arm)

Dire wolves can use double attack and dismember, but do not get a ranged attack

Trolls get a melee (club smash) and a ranged (boulder throw) but don't get dismember because their Int is too low for a special

Imp/goblins would get melee + ranged, and get double strike but not dismember (Stregth to low)

Demons get Melee + Magic and get dismember + AOE

Need to build a matix of what stats give what specials as an option and then give a way to set the name for those specails

also need to have a way to determine the base 3 grades of char

## Stat-Based Attack System (Rough Sketch)

Basic attack threshold: 3+ in stat
Special attack threshold: 6+ in stat  
Mastery bonus threshold: 9+ in stat

STR 6+ = Dismember special
INT 6+ = AOE special
AGL 6+ = Double Strike special

STR 9+ = 20% instant kill on dismember (non-special enemies)
INT 9+ = 20% paralyze all on AOE
AGL 9+ = 50% chance for triple strike

## Example Enemy JSON Structure
```json
{
    "name": "Shadow Drake",
    "strength": 7,
    "intellect": 8,
    "agility": 5,
    "attack_names": {
        "melee": "Shadow Claw",
        "ranged": "Wing Buffet", 
        "magic": "Dark Breath",
        "special_str": "Eviscerate",
        "special_int": "Shadow Storm",
        "special_agl": null
    }
}
```

Attack availability determined by stats:
- Can use melee (STR 7 > 3)
- Can use ranged (AGL 5 > 3)  
- Can use magic (INT 8 > 3)
- Gets Dismember special (STR 7 > 6)
- Gets AOE special (INT 8 > 6)
- No Double Strike (AGL 5 < 6)



also want to add elementals to magic use (frost will reduce atk after 3 attacks, or 5% chance to freeze, persistent burning damange (10 per turn for 3 turns), elctric (15% chance to paralize?))

add more flavor to melee and ranged attacks (heavy/ light wepons)(consumables?)

want to add resistences.

Add human actors have the option to have potions and gold?

add enememy loot?

add leveling system based on damage taken and damage dealt