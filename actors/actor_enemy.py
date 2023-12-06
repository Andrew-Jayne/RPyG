from actors.actor import Actor
from actors.actor_combatant import Combatant

class Enemy(Actor, Combatant):
    def __init__(self, 
                 name:str, 
                 health:int, 
                 strength:int, 
                 intellect:int, 
                 agility:int, 
                 luck:int, 
                 attack_name:str):
        attack_power = __class__._set_enemy_attack_power(strength,intellect)

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

    def _set_enemy_attack_power(strength,intellect):
        try:
            if strength > intellect:
                attack_power = strength
            else:
                attack_power = intellect
            return attack_power * 10
        except:
            import pdb; pdb.set_trace()
