# This module is for static, or single update constants, this allows values to be avalible without class or module imports
# This is a default value that should be can be updated to "MANUAL" during the welcome function


from typing import Literal, Self


class Config:
    _instance: Self | None = None  # Class variable with = None
    _global_game_mode: Literal["AUTO", "MANUAL"] = "AUTO"
    _debug_enabled: bool = False

    def __init__(
        self, global_game_mode: Literal["AUTO", "MANUAL"], debug_enabled: bool
    ):
        if Config._instance is None:
            Config._global_game_mode = global_game_mode
            Config._debug_enabled = debug_enabled
            Config._instance = self
        print("initied config")

    @property
    def global_game_mode(self) -> Literal["AUTO", "MANUAL"]:
        return self._global_game_mode

    @global_game_mode.setter
    def global_game_mode(self, mode: Literal["AUTO", "MANUAL"]) -> None:
        if mode not in ["AUTO", "MANUAL"]:
            raise ValueError(
                f"Mode: {mode} is not a valid option for global_game_mode must be either 'AUTO' or 'MANUAL'"
            )
        self._global_game_mode = mode

    @property
    def debug_enabled(self) -> bool:
        return self._debug_enabled

    @debug_enabled.setter
    def debug_enabled(self, mode: bool) -> None:
        match mode:
            case False:
                self._debug_enabled = False
            case True:
                self._debug_enabled = True
            case _:
                raise ValueError(f"Invalid Option for Debug Enabled {mode}")

    @classmethod
    def get_config(cls):
        if Config._instance is not None:
            return Config._instance
        else:
            raise RuntimeError(
                "Attempted to access Config instance before initialization"
            )
