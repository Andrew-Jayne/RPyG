Think like a classic API

The UI is there for presentation, but it never creates data, and the data should not be opinonated on HOW it is displayed but should include enough data to let an interface understand how it SHOULD be displayed.

Base concept there are 2 content channels, and one is bi-directonal

**Output Channel**
CoreIO.send_output("My name is ツ) -> RPyGInterface.send_output()

**Input Channel**
"I want a player name"
        CoreIO.request_input() -> RPyGInterface.request_input() V
                                                                V "The player's name is x86Jawa" (stored in a buffer)
value = CoreIO.receive_input() -> RPyGInterface.receive_input() V
"The player's name is x86Jawa"