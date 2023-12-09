from welcome import *

from actors.actor_party import *
from actors.actor_playable import *

#my_party = party_start()

player_party_instance = PlayerParty("The Default Party", default_party())

for member in player_party_instance.members:
    print(type(member))
    print(member[0])
    print(member[1])


print(player_party_instance.__dict__)


