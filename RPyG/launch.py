from RPyG.core_io import RPyGInterface
from RPyG.interfaces import BasicTerminalInterface


def launch_game() -> None:
    from RPyG.content import ContentLibrary
    from RPyG.core_io import CoreIO

    interface: RPyGInterface = BasicTerminalInterface()

    global_core_io = CoreIO(interface)
    global_core_io.validate()  # pyright: ignore[reportUnusedCallResult]

    global_content_library = ContentLibrary(interface.get_content_data())
    global_content_library.validate_content()

    global_game_state = interface.get_game_state()
    global_game_state.validate()  # pyright: ignore[reportUnusedCallResult]

    global_game_state.play_game()
