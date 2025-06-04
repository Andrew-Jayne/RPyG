# This module is for static, or single update constants, this allows values to be avalible without class or module imports
# This is a default value that should be can be updated to "MANUAL" during the welcome function

from typing import Literal

GLOBAL_GAME_MODE = "AUTO"
DEBUG_ENABLED = False


def update_global_game_mode(mode: Literal["AUTO", "MANUAL"]) -> None:
    """
    Simple Setter Function for the Global Game Mode
    Any Values other than Auto & Manual will raise a ValueError
    """

    if mode not in ["AUTO", "MANUAL"]:
        raise ValueError("Mode value not in ['AUTO', 'MANUAL']")
    else:
        global GLOBAL_GAME_MODE
        GLOBAL_GAME_MODE = mode


def set_debug(enabled: bool = False) -> None:
    """
    allows debug mode to be enabled
    """
    global DEBUG_ENABLED
    if enabled is True:
        global DEBUG_ENABLED
    else:
        pass
