from actor_playable import PlayableActor
import random

class Follower(PlayableActor):

    def __init__(self, name:str, strength:int, intellect:int):
        ## Setup Player Stats
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