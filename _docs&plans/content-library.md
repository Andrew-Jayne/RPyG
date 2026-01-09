Everything goes in to the content library, and it validates and links all content, kinda like a compiler. the structure is like this


```python
class ContentLibrary:
    enemies: dict[str, Enemy]
    enemy_sets: dict[str, EnemySet]
    story_events: dict[str, StoryEvent]
    encounters: dict[str, Encounter]
    encounter_effects: dict[str, EncounterEffect]
    dungeons: dict[str, Dungeon]
```

Each of these corresponds to a TOML file which provides a normalised format for data storage.
**TOML does not have a null value** 
so `type | None = None` is used for optional feilds

The directory structure is arbiraty and all files with a .toml extension in a directory below the set `content_directory` value will be loaded, this is desinged to make adding mod-packs or other content add-on's simple as a user can simply add or replace the files in the directory.

Examples of each type of object that is declared.
These are meant to roughly model a k8s resorce, but use TOML instead of YAML.

PyYAML is not in the STD python lib.
JSON lacks comments and allows for deep nested structures than can be awkward to read.
TOML Forces a design pattern, and that pattern aligns with constucts within the application

## Dungeon
```toml
[witch_tower]
kind = "Dungeon/v1"
name = "Witch's Tower"
length = 7
boss_enemy_id = "thunder_demon_lord"
enemy_set_id = "valericas_minions"
start_message = "The party finds a stone tower with a pulsing green light eminating from the top"
shortcut_message = "The party Find a secret passage!"
heal_room_message = "The party finds a alchemy lab with food & potions!"
boss_encounter_message = """
You find Valerica the High preistess a top the tower. 
The green light is eminating from her as you move forward the light turns blood red and her body evaporates. 
When she stood a hulking Demonic Figure Roars as a storm gathers around the tower
"""
```

## Encounter Effect
```toml
[heal_30]
kind = "EncounterEffect/v1"
actor_action = "HEAL"
targets = "ALL"
magnitude = 30
effect_messages = []
extra_effects = []
```

## Encounter
```toml
[rest_small_refuge]
kind = "Encounters/v1"
primary_encounter = true
special_encounter = false
# next_encounter = None
prompts = ["Your Party finds a Small Refuge"]
success_choice = "REST"
# retry_choice = None
failure_choice = "LEAVE"
success_effects = ["heal_30"]
retry_effects = []
failure_effects = []
success_messages = ["They Make camp for the night"]
retry_messages = []
failure_messages = ["They Travel onwards"]
```

## Enemy
```toml
[stunted_cave_troll]
kind = "Enemy/v1"
name = "Stunted Cave Troll"
variant_grade = "LESSER"
health = 200
strength = 7
intellect = 1
agility = 1
luck = 1
attack_name = "Club Smash"
is_special = false
```

## Enemy Set
```toml
["cave_trolls"]
kind = "EnemySet/v1"
plural_name = "Cave Trolls"
group_name = "Gang"
weight_class = "LARGE"
set_type = "STANDARD"
# key_enemy = None
enemy_ids = [
    "cave_troll_chief",
    "cave_troll",
    "stunted_cave_troll",
    "ancient_cave_troll",
]
```


## Story Event
```toml
["tavern_quest_notice_event"]
kind = "StoryEvent/v1"
progress_trigger = 1
event_type = "ENCOUNTER"
encounter_id = "tavern_quest_notice"
# enemy_id = None
# dungeon_id = None
messages = [
    "{party_name} gathers around the fire at a local tavern when a rider delivers a notice to the bar keep",
    "the notice reads:",
    "His Highness King Stallman has requested all who favor themselves brave warriors present themselves at the Open Hall as the king has a task which requires great courage for them to undertake.",
    "After seeing the kings missive the path ahead is clear.",
    ]
success_messages = [
  "And thus {party_name} began their quest.",
  "If only they knew the trials and triumphs that lay ahead..."
]
failure_messages = []
```