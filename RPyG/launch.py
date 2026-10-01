from logging import getLogger

from RPyG.core_io import RPyGInterface
from RPyG.interfaces import BasicTerminalInterface
from RPyG.log_file import setup_logging


logger = getLogger(__name__)


def launch_game() -> None:
    from RPyG.content import ContentLibrary
    from RPyG.core_io import CoreIO

    LOG_PATH = setup_logging()
    logger.info("opening new log file at %s", LOG_PATH)

    interface: RPyGInterface = BasicTerminalInterface()

    GLOBAL_CORE_IO = CoreIO(interface)
    GLOBAL_CORE_IO.validate()  # pyright: ignore[reportUnusedCallResult]
    logger.info("CoreIO validated, using %s interface", interface.__class__.__name__)

    GLOBAL_CONTENT_LIBRARY = ContentLibrary(interface.get_content_data())
    GLOBAL_CONTENT_LIBRARY.validate_content()
    logger.info(
        "Content Library validated, total objects %s",
        GLOBAL_CONTENT_LIBRARY.total_items(),
    )

    GLOBAL_GAME_STATE = interface.get_game_state()
    GLOBAL_GAME_STATE.validate()  # pyright: ignore[reportUnusedCallResult]

    GLOBAL_GAME_STATE.play_game()
