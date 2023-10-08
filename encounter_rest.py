import random
from interaction import Interaction


class RestEncounters():
    
    @staticmethod
    def rest_encounter(player_instance):
        rest_chance = random.randint(0,3)
        if rest_chance in range(0,2):
            print("You Find a Tavern and Rest for a short time")
            player_instance.heal(5)
            print(f"Your Health is now {player_instance.health}") 
        elif rest_chance == 2:
            print("You Find an Inn and Rest for the evening")
            player_instance.heal(7)
            print(f"Your Health is now {player_instance.health}") 
        elif rest_chance == 3:
            print("You Find the King's Vassal's Keep, and take a day to rest, and replenish your supplies.")
            player_instance.heal(9)
            print(f"Your Health is now {player_instance.health}") 
            Interaction.at_merchant(player_instance)