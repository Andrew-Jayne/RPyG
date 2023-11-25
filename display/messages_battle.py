def battle_hud_message(player_instance, enemy_instance):
    print(f"{player_instance.name}: {player_instance.health}")
    if player_instance.has_follower == True:
        print(f"{player_instance.follower_instance.name}: {player_instance.follower_instance.health}")
    print(f"{enemy_instance.name}: {enemy_instance.health}")

def battle_start_message():
    print("The Battle Begins!", end="\n\n\n")