from RPyG.core_io import RPyGInterface
from RPyG.utilities import ensure_type, setup_logger


logger = setup_logger(__name__)


def launch_game(
    interface: RPyGInterface,
) -> None:
    from RPyG.content import ContentLibrary
    from RPyG.core_io import CoreIO
    from RPyG.run_game import play_game

    ensure_type(interface, RPyGInterface, "interface")
    # These are gateway singletons so we just need to create them
    # at a scope where they live for the lifetime of the application

    logger.info("CoreIO starting")
    global_core_io = CoreIO(interface)
    logger.info("Validating CoreIO")
    global_core_io.validate
    logger.info("CoreIO validated")
    logger.info("CoreIO ready")

    logger.info("ContentLibrary starting")
    global_content_library = ContentLibrary(interface.get_content_data())
    logger.info("Validating ContentLibrary")
    global_content_library.validate_content()
    logger.info("ContentLibrary validated")
    logger.info("ContentLibrary ready")

    logger.info("Loading GameState")
    global_game_state = interface.get_game_state()
    logger.info("Validating GameState")
    global_game_state.validate()
    logger.info("GameState validated")
    logger.info("GameState ready")

    logger.info("All startup checks passed")
    logger.info("Starting game mode with %s interface", interface.__class__.__name__)
    play_game()
