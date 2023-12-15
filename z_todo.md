## V2 Goals
[*] RPC for Mystery Encounters
[*] Merge Rest & Mystery Encounters
[] Add Defend, Evade, Elude for secondary combat action
[] Finish Merchant Interaction
[] Polish Special Encounters 
[*] Remove all remaining "You" Messages
[*] Remove Follower
[*] Add Randomness to Damage
[*] Remove direct prints from rest and mystery encounters
[] expand merchant system
[] Move special encounter to line up with new json fommating
[] Specalization based Attack Names (3 grades)
[] Sweep for junk funcitons &| bloat
[] Add enemy AIs



## Stretch Goals
[] add AOE attack that can hit all enemy or player instances
[] add leveling system based on battle actions
[] add 2nd attack type for each class with new names
[] add damage type (Magic, Melee) + Resistances based on Specalization
[] add multi action encounters (you rest for the night but are robbed in your sleep and lose all of your gold!)


## Multi-Action Encoutner Concept

```json

{ 
    "events": [
        {
    "event_id": "event1",
    "event_attribuites": {
        "stuff" : null,
        "addional_events": null
    }},{
    "event_id": "event2",
    "event_attributes": {
        "stuff" : null,
        "addional_events": null
    }},{
    "event_id": "event3",
    "event_attributes": {
        "stuff" : null,
        "addional_events": ["event1", "event2"]
    }}
    ]
}
```

```python
if active_event_attributes[addional_events] != None:
    run_event(event_attributes)
```