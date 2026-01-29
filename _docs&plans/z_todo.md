Add Logging!!
Move interface interaction to all used 0-N indexed choices rather than typing the action every time (so you can play 1 handed with a numpad)
Move all output text to Semantic data rather than pure text

Rework Player Party & Save system to use SQLite instead of Pickle, to prevent command injection by malicious actors (If I wanted to I can hack a save file and os.remove_tree(/) and nuke the server or another users computer)
Build dehydrate Rehydrate system for player party

in_dungeon: bool
dungeon_id: str
dungeon_progress: int

removes the jank composition thing of sticking a dungeon inside a player party lol