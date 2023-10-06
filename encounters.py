import random

class Encounters:
    def __init__(self, player_instance):
        self.player_instance = player_instance

    @staticmethod
    def print_health(player_instance):
        print(f"Your Health is now {player_instance.health}")   

    @staticmethod
    def check_for_encounter(player_instance):

        encounter_check = random.uniform(0, 1)

        if 0 <= encounter_check < 0.125:  # First 12.5% range
            EnemyEncounters.enemy_encounter(player_instance)
            __class__.print_health(player_instance)
            
        elif 0.125 <= encounter_check < 0.25:  # Second 12.5% range
            RestEncounters.rest_encounter(player_instance)
            __class__.print_health(player_instance)
            
        elif 0.25 <= encounter_check < 0.375:  # Third 12.5% range
            MysteryEncounters.mystery_encounter(player_instance)
            __class__.print_health(player_instance)

    


class RestEncounters(Encounters):
    def __init__(self, player_instance):
        super().__init__(player_instance)
    
    @classmethod
    def rest_encounter(self ,player_instance):
        print("You Find an Inn and Rest")
        player_instance.heal(5)


class EnemyEncounters(Encounters):
    def __init__(self, player_instance):
        super().__init__(player_instance)
    
    @classmethod
    def enemy_encounter(self, player_instance):
        print("An Enemy was encountered!")
        player_instance.damage(5)
        

class MysteryEncounters(Encounters):
    def __init__(self, player_instance):
        super().__init__(player_instance)
    
    @classmethod
    def mystery_encounter(self, player_instance):
        print("You Encounter A Strange Figure!")
        mystery_chance = random.randint(0,1)
        if mystery_chance == 0:
            player_instance.heal(3)
            print("The Figure heals you and vanishes into the darkness!")
        else:
            player_instance.damage(3)
            print("The Figure blasts you with an Arcane Bolt and vanishes into a Flash of Light!")