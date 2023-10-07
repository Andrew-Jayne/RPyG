class Interaction:
    def __init__(self):
        pass

    @staticmethod
    def post_combat(player_instance):
        if player_instance.health < 20 and player_instance.potions != 0:
            player_instance.use_potion()

    @staticmethod
    def in_combat(player_instance):
        if player_instance.health <= 4 and player_instance.potions != 0:
                player_instance.use_potion()
                return False
        else:
            print("You have no remaining potions and must make a stand!")
            return True

    @staticmethod
    def at_merchant(player_instance):
        while player_instance.potions > 9 and player_instance.gold != 0:
            player_instance.gold -= 25
            player_instance.potions += 1
            print(f"You purchase a potion. You now have {player_instance.potions}")

