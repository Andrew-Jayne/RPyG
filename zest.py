from welcome import *

from actors.actor_party import *
from actors.actor_playable import *
from actors.actor_player import *

my_party = party_start()

print(my_party)

for member in my_party:
    print(member.name)
    print(member.specialization)

my_party_instances = []
for member in my_party:
    party_member = Player(member.name, member.specialization)
    my_party_instances.append(party_member)



party_instances = Party(my_party_instances)

print(party_instances.__dict__)


[{'Player1', 'Warrior'}, {'Player2', 'Mage'}, {'Player3', 'Rogue'}]
