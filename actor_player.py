from actor_playable import PlayableActor
import random

class Player(PlayableActor):

    def __init__(self, name:str):
        ## Setup Player Stats
        strength = random.randint(1,10)
        intellect = random.randint(1,10)
        luck = random.randint(1,10)
        health = 10 + int((strength + intellect) * 2)
        gold = strength * 25
        potions = int(intellect / 2) 

        ## Init Inherited Classes
        PlayableActor.__init__(self, name=name, health=health, strength=strength, intellect=intellect, luck=luck, gold=gold, potions=potions)

        ## Copy values to instance
        self.name = name
        self.health = health
        self.strength = strength
        self.intellect = intellect
        self.attack_name = PlayableActor._set_attack_name(self)
        self.attack_power = PlayableActor._set_attack_power(self)
        self.has_follower = False
        self.follower_instance = None

    def gain_follower(self, follower_instance):
        self.has_follower = True
        self.follower_instance = follower_instance
        pass

    def lose_follower(self,follower_instance):
        print(f"{follower_instance.name} has fallen in combat", end="\n\n")
        self.has_follower = False
        self.follower_instance = None
    

