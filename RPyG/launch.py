from RPyG.core_io import RPyGInterface
from RPyG.utilities import ensure_type, setup_logger


logger = setup_logger(__name__)


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
    logger.info("ContentLibrary starting, with content_path: %s", content_path)
    ContentLibrary(content_path)  # pyright: ignore[reportUnusedCallResult]
    logger.info("ContentLibrary ready")

    logger.info("Validating ContentLibrary")
    ContentLibrary.validate_content()
    logger.info("ContentLibrary validated")

    logger.info("CoreIO starting")
    CoreIO(interface)  # pyright: ignore[reportUnusedCallResult]
    logger.info("CoreIO ready")

    logger.info("Starting game mode with %s interface", interface.__class__.__name__)
    play_game()
