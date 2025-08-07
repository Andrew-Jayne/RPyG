# Project Roadmap

***PR’s should do one thing and do it well.***

---

# Planned Development

- **Damage Types & Resistances:**
  - Implement damage types: Melee and Magic.
  - Create resistances based on character specialization 
    - higher INT provides more magic resistance
    - lower STR increases vulnerability to melee damage
  - Introduce hybrid attacks with customizable splits (e.g., a magic sword attack with a 60/40 split between magic and melee). (most likely need to bring back a modified verison of the skill system to select attack?)

- **Expanded Combat Mechanics:**
  - Add persistent effects (e.g., lingering damage, healing spells, defense buffs).
  - Create unique attacks for enemies based on their abilities.
  - Integrate persistent effects into the combat system.

- **Progression Logic:**
  - Use if logic in attack function (if target or if source is playable_actor) to update exp. 
  - After battle if exp passes threshold player levels up
  - On level-up:
    - Fully heal the player.
    - Allow the player to boost one stat by 1 point.
    - Update base health accordingly.

- **Relics System:**
  - Allow players to find or buy relics that boost party stats.
  - Implement a relic loot pool for enemies (1 in 25 chance) (part of the enemy JSON?)
  - Expand merchant system with relic offerings.
  - Implement party-wide relic boost functions.
  - Relics can also be stolen 

- **Non-Special Dungeons:**
    - Use the existing JSON schema for special dungeons.
    - Optionally, introduce random encounters ("You find a $dungeon_identify").
    - this needs more planning and work
  
- **Travel Encounter:**
  - Create a "TRAVEL" encounter type.
  - Logic based on total party STR, INT, or AGL to determine success or failure:
    - Success: Gain +3 progress.
    - Failure: Lose -2 progress.
  - Add decision-based progress events (e.g., shortcuts, with potential success/failure outcomes).
  - Ensure story events cannot be skipped when using shortcuts.
  - example: 
    - "you see a steep mountain pass that would save you 30 miles of travel do you think you are agile enough to traverse it?" (if party total AGL is over 18 success)

    - S: you traverse the pass saving 30 miles of travel
    - F: you become lost in the mountains and must back track wasting 20 miles of travel

- **Biome-Based Encounters:**
  - Based on being in the 0-25, 26-50, 51-75 & 76-99 progress zones
  - Create biome-specific encounters (forest, plains, foothills, mountains).
  - Tag encounters and enemies based on zones/biomes (frost drakes in mountains, dire wolves in plains).
  - Keep there from being major immersion violations due to RNG (like finding a big city a step 98 right before the final boss)


---

# Active Development

- **Streamline User Prompts:**
  - Develop a more generic "choose action" prompt template to avoid redundancy in designing individual interactions.
