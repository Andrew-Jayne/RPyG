from welcome import *

from actors.actor_party import *
from actors.actor_playable import *
from actors.actor_player import *

#my_party = party_start()

player_party_instance = PlayerParty("The Default Party", default_party())

for member in player_party_instance.members:
    print(type(member))
    print(member.name)
    print(member.specialization)


print(player_party_instance.__dict__)


