from RPyG.core_io import RPyGInterface
from RPyG.utilities import ensure_type


def launch_game(
    content_path: str,
    interface: RPyGInterface,
) -> None:
    from RPyG.content import ContentLibrary
    from RPyG.core_io import CoreIO
    from RPyG.game_state import play_game

    ensure_type(content_path, str, "content_path")
    ensure_type(interface, RPyGInterface, "interface")

    # These are gateway singletons so we just need to create them
    # at a scope where they live for the lifetime of the application
    ContentLibrary(content_path)
    ContentLibrary.validate_content()
    CoreIO(interface)
    play_game()
