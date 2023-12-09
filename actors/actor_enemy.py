from actors.actor import Actor
from actors.actor_combatant import Combatant

class Enemy(Actor, Combatant):
    def __init__(self, enemy_attributes:dict):
        
        name=enemy_attributes['name']
        health=enemy_attributes['health']
        strength=enemy_attributes['strength']
        intellect=enemy_attributes['intellect']
        agility=enemy_attributes['agility']
        luck=enemy_attributes['luck']
        attack_name=enemy_attributes['attack_name']
        attack_power = __class__.__set_enemy_attack_power(strength,intellect)

        ## Init Inherited Classes     
        Actor.__init__(self, 
                       name=name, 
                       strength=strength, 
                       intellect=intellect,
                       agility=agility,
                       luck=luck)
        Combatant.__init__(self,
                           health=health,
                           attack_name=attack_name,
                           attack_power=attack_power
                           )

    def __set_enemy_attack_power(strength,intellect):
            if strength >= 6 and intellect >= 6:
                attack_power = strength + intellect
            elif strength > intellect:
                attack_power = strength
            elif strength < intellect:
                attack_power = intellect
            else:
                 attack_power = int((strength + intellect) / 2)

            return attack_power * 10
