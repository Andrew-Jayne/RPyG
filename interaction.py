class Interaction:
    def __init__(self):
        pass

    @staticmethod
    def post_battle(player_instance):
        if player_instance.health < 20 and player_instance.potions != 0:
            player_instance.use_potion()

    @staticmethod
    def in_battle(player_instance):
        if player_instance.health <= 4 and player_instance.potions != 0:
                player_instance.use_potion()
                return False
        elif player_instance.potions == 0:
                print("You have no remaining potions and must make a stand!")
                return True
        else:
            return True

    @staticmethod
    def at_merchant(player_instance):
        while player_instance.potions < 100 and player_instance.gold != 0:
            if player_instance.gold != 0:
                player_instance.gold -= 25
                player_instance.potions += 1
                print(f"You purchase a potion. You now have {player_instance.potions}")
            else:
                 print("You do not have enough Gold to purchase more potions")
                 break

