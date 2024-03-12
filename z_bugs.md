using double strike throws this error when attacking the same target twice and it dies on the first attack 
```
Traceback (most recent call last):
  File "/Users/andrewjayne/Projects/RPyG/main.py", line 71, in <module>
    main(mode,use_default)
  File "/Users/andrewjayne/Projects/RPyG/main.py", line 40, in main
    if check_for_encounter(player_party_instance, rounds_without_encounter) == False:
       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/andrewjayne/Projects/RPyG/encounters/encounter.py", line 18, in check_for_encounter
    enemy_encounter(player_party_instance)
  File "/Users/andrewjayne/Projects/RPyG/encounters/encounter_enemy.py", line 60, in enemy_encounter
    Combat.battle(player_party_instance, enemy_party)
  File "/Users/andrewjayne/Projects/RPyG/combat/combat.py", line 101, in battle
    __class__.process_player_turn(player_party_instance,enemy_party_instance)
  File "/Users/andrewjayne/Projects/RPyG/combat/combat.py", line 48, in process_player_turn
    special_attack(player_instance, enemy_party_instance)
  File "/Users/andrewjayne/Projects/RPyG/combat/combat_actions.py", line 165, in special_attack
    double_attack(attacker_instance,target_party_instance)
  File "/Users/andrewjayne/Projects/RPyG/combat/combat_actions.py", line 130, in double_attack
    target_party_instance.lose_member(secondary_instance)
  File "/Users/andrewjayne/Projects/RPyG/actors/actor_party.py", line 19, in lose_member
    self.members.remove(member)
ValueError: list.remove(x): x not in list
```

Should just need a check to make sure targets are alive before trying to attack (this was also the last enemy)