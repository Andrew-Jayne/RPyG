import random

# Only used for Type Checking
from actors.actor_party import Party

def select_combat_target(target_party_instance:Party) -> int:
    if not isinstance(target_party_instance, Party):
        raise ValueError("The 'target_party_instance' parameter must be of type Party. Received type: {}".format(type(target_party_instance).__name__))

    """
    Takes a full party instance, and returns the index of the target member in the members array/list as an int
    """


    target_party_members = target_party_instance.members
    method_id = random.choice(["MAX_ATK","MIN_HP","RANDOM"])
    match method_id:
        case "MAX_ATK":
            target_attributes_list = []
            for index,member in enumerate(target_party_members):
                target_attributes = (index,member.attack_power)
                target_attributes_list.append(target_attributes)
            sorted_target_attributes_list = sorted(target_attributes_list, key=lambda x: x[1], reverse=True)
            return sorted_target_attributes_list[0][0]
        
        case "MIN_HP":
            target_attributes_list = []
            for index,member in enumerate(target_party_members):
                target_attributes = (index,member.health)
                target_attributes_list.append(target_attributes)
            sorted_target_attributes_list = sorted(target_attributes_list, key=lambda x: x[1])
            return sorted_target_attributes_list[0][0]
        
        case "RANDOM":
            return random.randint(0,(len(target_party_members) - 1))
        case _:
            raise ValueError("Big Problem in Select_Target, Go buy a lotto ticket")