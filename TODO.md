# RPyG Refactor TODO List

## Encounter System Migration
- [ ] Fix encounter system integration in launch.py - update line 121 to use new process_encounter() method
- [ ] Update all encounter references to use the new Encounter class instead of old one
- [ ] Remove encounter_old.py after migration is complete
- [ ] Fix duplicate class definitions (SpecialAction, ActorAction, Encounter, EncounterEffect in encounter_old.py)

## Dungeon System Updates
- [ ] Refactor dungeon.py to use new encounter system instead of old encounter methods
- [ ] Replace hardcoded dungeon encounter logic with content-driven approach
- [ ] Integrate dungeon encounters with new EncounterEffect system

## Interface Cleanup
- [ ] Remove legacy code block (lines 203-513) from terminal_interface.py
- [ ] Verify all interface calls use the new CoreIO system properly

## Testing & Verification
- [ ] Test game in AUTO mode to verify encounters work
- [ ] Test game in MANUAL mode to verify encounters work
- [ ] Verify all content loads correctly from TOML files

## Minor Fixes
- [ ] Fix typo in rest_palace.toml (line 86: 'Youzr' should be 'Your')

## Notes
- You were in the middle of a double refactor (content system + interface system)
- The content system refactor is mostly complete (TOML loading works)
- Main issue: new encounter system isn't fully integrated, old system still being called in places
- Dungeons are broken because they use the old encounter mechanics
- The new system structure is much cleaner once fully migrated