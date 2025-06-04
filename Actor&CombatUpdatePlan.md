Things to fix:

Make the Combatant a subclass of actor (it was supposed to be lol)

Make Enemy and Playable Actor inherit from Combatant


Inventory becomes an object mounted at player.inventory rather than a subclass

Add combatant party from which both Enemy Party and PlayerParty inherit from


move all combat actions into a fucntions file used by the combant class, this should make the combat module much simpler

move select target into the combatant class (moving towards strategy pattern)