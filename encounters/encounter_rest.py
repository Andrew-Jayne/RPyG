import random
from interaction.interaction import Interaction


class RestEncounters():
    
    @staticmethod
    def rest_encounter(player_instance):
        rest_chance = random.randint(0,3)
        if rest_chance in range(0,2):
            print("You Find a Tavern and Rest for a short time", end="\n\n")
            player_instance.heal(5)
        elif rest_chance == 2:
            print("You Find an Inn and Rest for the evening", end="\n\n")
            player_instance.heal(7)
        elif rest_chance == 3:
            print("""
You Find A Vassal's Keep!
You take a day to rest, and replenish your supplies.
""", end="\n\n")
            player_instance.heal(9)
            Interaction.at_merchant(player_instance)