from actors.actor import Actor
from actors.actor_combatant import Combatant
import random

class Inventory:
    def __init__(self, gold:int, potions:int):
        self.gold = gold
        self.potions = potions

class PlayableActor(Actor, Inventory, Combatant):
    def __init__(self, 
                 name: str, 
                 specialization: str,
                 health: int, 
                 strength: int, 
                 intellect: int, 
                 agility:int, 
                 luck: int, 
                 gold:int, 
                 potions:int):

    ## Init Inherited Classes
        Actor.__init__(self, 
                       name=name,
                       strength=strength, 
                       intellect=intellect, 
                       agility=agility, 
                       luck=luck)

        Inventory.__init__(self, 
                           gold=gold, 
                           potions=potions)
        
        Combatant.__init__(self, 
                           health=health,
                           attack_name=__class__._set_attack_name(self),
                           attack_power=__class__._set_attack_power(self)
                           )


    def use_potion(self):
        if self.potions != 0:
            print("You drink a potion")
            self.potions -= 1
            self.heal(10 + random.randint(-2,2))
            print(f"You have {self.potions} remaining")
            print(f"Your health is now {self.health}", end="\n\n")
        else:
            print("You have no remaining potions!")

    def _set_attack_power(self):
        if self.strength > self.intellect:
            self.attack_power = self.strength
        elif self.strength >= 7 and self.intellect >= 7:
            self.attack_power = int(self.strength + self.intellect * .75)
        else:
            self.attack_power = self.intellect

        return self.attack_power * 10

    def _get_skill(self):
        strength_skill = ""
        intellect_skill = ""
        player_skill = ""

        if self.strength in range(1, 4):
            strength_skill = "weak"
        elif self.strength in range(4, 7):
            strength_skill = "fair"
        elif self.strength in range(7, 10):
            strength_skill = "strong"
        elif self.strength == 10:
            strength_skill = "mighty"

        if self.intellect in range(1, 4):
            intellect_skill = "dull"
        elif self.intellect in range(4, 7):
            intellect_skill = "ordinary"
        elif self.intellect in range(7, 10):
            intellect_skill = "smart"
        elif self.intellect == 10:
            intellect_skill = "brilliant"
                
        player_skill = str(f"{strength_skill}:{intellect_skill}")

        return player_skill
    
    def _set_attack_name(self):
        player_skill = __class__._get_skill(self)

        match player_skill:
            case "weak:dull":
                self.attack_name = "Clumsy Punch"
            case "fair:dull":
                self.attack_name = "Axe Chop"
            case "strong:dull":
                self.attack_name = "Warhammer Slam"
            case "mighty:dull":
                self.attack_name = "Greatsword Cleave"

            case "weak:ordinary":
                self.attack_name = "Dagger Slash"
            case "fair:ordinary":
                self.attack_name = "Shorsword Slash"
            case "strong:ordinary":
                self.attack_name = "Longsword Thrust"
            case "mighty:ordinary":
                self.attack_name = "Greatsword Thrust"

            case "weak:smart":
                self.attack_name = "Arcane Bolt"
            case "fair:smart":
                self.attack_name = "Fireball"
            case "strong:smart":
                self.attack_name = "Arcane Longsword Strike"
            case "mighty:smart":
                self.attack_name = "Arcane Greatsword Cleave"

            case "weak:brilliant":
                self.attack_name = "Arcane Lighting"
            case "fair:brilliant":
                self.attack_name = "Great Fireball"
            case "strong:brilliant":
                self.attack_name = "Seismic Hammer Slam"
            case "mighty:brilliant" :
                self.attack_name = "Cosmic Greatsword Cleave"

        return self.attack_name