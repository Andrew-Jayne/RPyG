from actors.actor import Actor
from actors.actor_combatant import Combatant

class Enemy(Actor, Combatant):
    def __init__(self, enemy_attributes:dict) -> None:

        if not isinstance(enemy_attributes['name'], str):
            raise ValueError("The 'enemy_attributes['name']' parameter must be of type str. Received type: {}".format(type(enemy_attributes['name']).__name__))
        if not isinstance(enemy_attributes['health'], int):
            raise ValueError("The 'enemy_attributes['health']' parameter must be of type int. Received type: {}".format(type(enemy_attributes['health']).__name__))
        if not isinstance(enemy_attributes['strength'], int):
            raise ValueError("The 'enemy_attributes['strength']' parameter must be of type int. Received type: {}".format(type(enemy_attributes['strength']).__name__))
        if not isinstance(enemy_attributes['intellect'], int):
            raise ValueError("The 'enemy_attributes['intellect']' parameter must be of type int. Received type: {}".format(type(enemy_attributes['intellect']).__name__))
        if not isinstance(enemy_attributes['agility'], int):
            raise ValueError("The 'agility=enemy_attributes['agility']' parameter must be of type int. Received type: {}".format(type(agility=enemy_attributes['agility']).__name__))
        if not isinstance(enemy_attributes['luck'], int):
            raise ValueError("The 'enemy_attributes['luck']' parameter must be of type int. Received type: {}".format(type(enemy_attributes['luck']).__name__))
        if not isinstance(enemy_attributes['attack_name'], str):
            raise ValueError("The 'enemy_attributes['attack_name']' parameter must be of type str. Received type: {}".format(type(enemy_attributes['attack_name']).__name__))

        name=enemy_attributes['name']
        health=enemy_attributes['health']
        strength=enemy_attributes['strength']
        intellect=enemy_attributes['intellect']
        agility=enemy_attributes['agility']
        luck=enemy_attributes['luck']
        attack_name=enemy_attributes['attack_name']
        is_special=enemy_attributes[is_special]
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

    def __set_enemy_attack_power(strength:int ,intellect:int) -> int:
            if strength >= 6 and intellect >= 6:
                attack_power = strength + intellect
            elif strength > intellect:
                attack_power = strength
            elif strength < intellect:
                attack_power = intellect
            else:
                 attack_power = int((strength + intellect) / 2)

            return attack_power * 10
