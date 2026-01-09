
  
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
