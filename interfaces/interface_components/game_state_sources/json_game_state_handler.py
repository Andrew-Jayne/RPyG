from typing import Final, TypedDict, cast, overload, override

from interfaces.interface_components.game_state_sources.abstract_game_state_handler import (
    GameStateHandler,
)
from RPyG.constructs import (
    BorrowTrackedResource,
    Dungeon,
    EnemyActor,
    EnemyParty,
    PlayableActor,
    PlayerParty,
)
from RPyG.constructs.actor.actor_components import Inventory
from RPyG.game_state import GameState
from RPyG.utilities import ensure_type


class InventoryDict(TypedDict):
    gold: int
    potions: int
    actor_name: str


class PlayerDict(TypedDict):
    name: str
    strength: int
    intellect: int
    agility: int
    luck: int
    health: int
    base_health: int
    attack_name: str
    attack_power: int
    special_attack_name: str
    special_attack_energy: int
    specialization: str
    use_special_attack: bool
    will_react: bool
    is_dismembered: bool
    react_action: str
    react_messages: dict[str, str]
    inventory: InventoryDict


class PlayerPartyDict(TypedDict):
    name: str
    members: list[PlayerDict]
    dead_members: list[PlayerDict]


class EnemyDict(TypedDict):
    name: str
    strength: int
    intellect: int
    agility: int
    luck: int
    health: int
    base_health: int
    attack_power: int
    special_attack_name: str
    special_attack_energy: int
    specialization: str
    use_special_attack: bool
    will_react: bool
    is_dismembered: bool
    attack_name: str
    is_special: bool
    variant_grade: str


class EnemyPartyDict(TypedDict):
    name: str
    members: list[EnemyDict]
    dead_members: list[EnemyDict]


class DungeonDict(TypedDict):
    name: str
    kind: str
    start_message: str
    shortcut_message: str
    heal_room_message: str
    boss_encounter_message: str
    boss_enemy_id: str
    enemy_set_id: str
    length: int
    special_dungeon: bool


class BorrowTrackedEnemyPartyDict(TypedDict):
    _resource: EnemyPartyDict | None
    _borrow_count: int


class BorrowTrackedDungeonDict(TypedDict):
    _resource: DungeonDict | None
    _borrow_count: int


class GameStateDict(TypedDict):
    player_party: PlayerPartyDict
    progress: int
    dungeon_progress: int | None
    enemy_party: BorrowTrackedEnemyPartyDict
    dungeon: BorrowTrackedDungeonDict


def dump_enemy(enemy_list: list[EnemyActor]) -> list[EnemyDict]:
    enemy_dicts: list[EnemyDict] = []
    for enemy in enemy_list:
        enemy_dicts.append(
            {
                "name": enemy.name,
                "strength": enemy.strength,
                "intellect": enemy.intellect,
                "agility": enemy.agility,
                "luck": enemy.luck,
                "health": enemy.health,
                "base_health": enemy.base_health,
                "attack_name": enemy.attack_name,
                "attack_power": enemy.attack_power,
                "special_attack_name": enemy.special_attack_name,
                "special_attack_energy": enemy.special_attack_energy,
                "specialization": enemy.specialization,
                "use_special_attack": enemy.use_special_attack,
                "will_react": enemy.will_react,
                "is_dismembered": enemy.is_dismembered,
                "is_special": enemy.is_special,
                "variant_grade": enemy.variant_grade.value,
            }
        )
    return enemy_dicts


def dump_dungeon(dungeon: Dungeon) -> DungeonDict:
    return {
        "name": dungeon.dungeon_name,
        "kind": "Dungeon/v1",
        "boss_encounter_message": dungeon.boss_encounter_message,
        "boss_enemy_id": dungeon.boss_enemy_id,
        "enemy_set_id": dungeon.enemy_set_id,
        "heal_room_message": dungeon.heal_room_message,
        "length": dungeon.length,
        "shortcut_message": dungeon.shortcut_message,
        "special_dungeon": dungeon.special_dungeon,
        "start_message": dungeon.start_message,
    }


def dump_enemy_party(enemy_party: EnemyParty) -> EnemyPartyDict:
    return {
        "name": enemy_party.name,
        "members": dump_enemy(enemy_party.members),
        "dead_members": dump_enemy(enemy_party.dead_members),
    }


@overload
def dump_borrow_tracked_resource(
    resource: BorrowTrackedResource[EnemyParty],
) -> BorrowTrackedEnemyPartyDict: ...


@overload
def dump_borrow_tracked_resource(
    resource: BorrowTrackedResource[Dungeon],
) -> BorrowTrackedDungeonDict: ...


def dump_borrow_tracked_resource(
    resource: BorrowTrackedResource[Dungeon] | BorrowTrackedResource[EnemyParty],
) -> BorrowTrackedEnemyPartyDict | BorrowTrackedDungeonDict:
    if resource._resource_type == Dungeon:  # pyright: ignore[reportPrivateUsage]
        resource = cast(BorrowTrackedResource[Dungeon], resource)
        if resource._resource is not None:  # pyright: ignore[reportPrivateUsage]
            return {
                "_resource": dump_dungeon(resource._resource),  # pyright: ignore[reportPrivateUsage]
                "_borrow_count": resource._borrow_count,  # pyright: ignore[reportPrivateUsage]
            }
        return {
            "_resource": None,
            "_borrow_count": 0,
        }
    if resource._resource_type == EnemyParty:  # pyright: ignore[reportPrivateUsage]
        resource = cast(BorrowTrackedResource[EnemyParty], resource)
        if resource._resource is not None:  # pyright: ignore[reportPrivateUsage]
            return {
                "_resource": dump_enemy_party(resource._resource),  # pyright: ignore[reportPrivateUsage]
                "_borrow_count": resource._borrow_count,  # pyright: ignore[reportPrivateUsage]
            }
        return {
            "_resource": None,
            "_borrow_count": 0,
        }

    raise ValueError(f"Unsupported Resource Type {str(resource._resource_type)}")  # pyright: ignore[reportPrivateUsage]


def dump_inventory(inventory: Inventory) -> InventoryDict:
    return {
        "gold": inventory.gold,
        "potions": inventory.potions,
        "actor_name": inventory.actor_name,
    }


def dump_player(players: list[PlayableActor]) -> list[PlayerDict]:
    player_dicts: list[PlayerDict] = []
    for player in players:
        player_dicts.append(
            {
                "name": player.name,
                "strength": player.strength,
                "intellect": player.intellect,
                "agility": player.agility,
                "luck": player.luck,
                "health": player.health,
                "base_health": player.base_health,
                "attack_name": player.attack_name,
                "attack_power": player.attack_power,
                "special_attack_name": player.special_attack_name,
                "special_attack_energy": player.special_attack_energy,
                "specialization": player.specialization,
                "use_special_attack": player.use_special_attack,
                "will_react": player.will_react,
                "is_dismembered": player.is_dismembered,
                "react_action": player.react_action,
                "react_messages": player.react_messages,
                "inventory": dump_inventory(player.inventory),
            }
        )
    return player_dicts


def dump_player_party(player_party: PlayerParty) -> PlayerPartyDict:
    return {
        "name": player_party.name,
        "members": dump_player(player_party.members),
        "dead_members": dump_player(player_party.dead_members),
    }


def build_game_state(save_data: GameStateDict) -> GameState:
    live_players: list[PlayableActor] = []
    for actor_data in save_data["player_party"]["members"]:
        actor_data["inventory"] = Inventory(**actor_data["inventory"])  # pyright: ignore[reportGeneralTypeIssues]
        live_players.append(PlayableActor(**actor_data))  # pyright: ignore[reportArgumentType]

    dead_players: list[PlayableActor] = []
    for actor_data in save_data["player_party"]["dead_members"]:
        actor_data["inventory"] = Inventory(**actor_data["inventory"])  # pyright: ignore[reportGeneralTypeIssues]
        dead_players.append(PlayableActor(**actor_data))  # pyright: ignore[reportArgumentType]

    game_state = GameState(
        player_party=PlayerParty(
            name=save_data["player_party"]["name"],
            members=live_players,
            dead_members=dead_players,
        ),
        progress=save_data["progress"],
        dungeon_progress=save_data["dungeon_progress"],
        dungeon=BorrowTrackedResource(Dungeon),
        enemy_party=BorrowTrackedResource(EnemyParty),
    )
    if save_data["dungeon"]["_resource"] is not None:
        game_state.set_dungeon(Dungeon(**save_data["dungeon"]["_resource"]))
    if save_data["enemy_party"]["_resource"] is not None:
        live_enemies: list[EnemyActor] = []
        for actor_data in save_data["enemy_party"]["_resource"]["members"]:
            live_enemies.append(EnemyActor(**actor_data))

        dead_enemies: list[EnemyActor] = []
        for actor_data in save_data["enemy_party"]["_resource"]["dead_members"]:
            dead_enemies.append(EnemyActor(**actor_data))
        game_state.set_enemy_party(
            EnemyParty(
                name=save_data["enemy_party"]["_resource"]["name"],
                members=live_enemies,
                dead_members=dead_enemies,
            )
        )
    return game_state


class JsonGameStateHandler(GameStateHandler):
    # """Secret""" key for HMAC, if you break your file that's on you
    SECRET_KEY: Final[bytes] = b"I_WILL_HACK_MY_SAVE_FILE_AND_PROBLEMS_WILL_BE_MY_FAULT"
    SAVE_FILE_PATH: Final[str] = "savegame.rpygs"

    @staticmethod
    def sign_save_file(data: bytes) -> bytes:
        import hashlib
        import hmac

        signature = hmac.new(
            JsonGameStateHandler.SECRET_KEY,
            data,
            hashlib.sha256,
        ).digest()

        return signature + data

    @staticmethod
    def check_save_file(data: bytes) -> bytes:
        import hashlib
        import hmac

        signature, serialized_data = data[:32], data[32:]  # Assuming SHA-256 hash
        expected_signature = hmac.new(
            JsonGameStateHandler.SECRET_KEY,
            serialized_data,
            hashlib.sha256,
        ).digest()
        if hmac.compare_digest(expected_signature, signature) is True:
            return serialized_data
        raise RuntimeError("Save file tampered with or corrupted.")

    @staticmethod
    def serialize_game_state(game_state: GameState) -> GameStateDict:

        ensure_type(game_state, GameState, "game_state")
        return {
            "player_party": dump_player_party(game_state.player_party),
            "progress": game_state.progress,
            "dungeon_progress": game_state._dungeon_progress,  # pyright: ignore[reportPrivateUsage]
            "dungeon": dump_borrow_tracked_resource(game_state._dungeon),  # pyright: ignore[reportPrivateUsage]
            "enemy_party": dump_borrow_tracked_resource(game_state._enemy_party),  # pyright: ignore[reportPrivateUsage]
        }

    @override
    @staticmethod
    def load_game_state() -> GameState:
        import os
        from json import loads

        from RPyG.core_io import CoreIO, output_models

        core_io = CoreIO.get_core_io()

        # Check if the save file exists
        if os.path.exists(JsonGameStateHandler.SAVE_FILE_PATH) is False:
            raise FileNotFoundError(
                "Save file not found. Please check file path & try again, or start a new game"
            )

        with open(JsonGameStateHandler.SAVE_FILE_PATH, "rb") as save_file:
            trimmed_save_data: GameStateDict = loads(
                JsonGameStateHandler.check_save_file(save_file.read())
            )

        game_state = build_game_state(trimmed_save_data)
        ensure_type(game_state, GameState, "GameState")
        core_io.send_output(
            output_models.OutputMessage(
                message=f"Successfully Loaded Save Game for: {game_state.player_party.name}"
            )
        )

        return game_state

    @override
    @staticmethod
    def save_game_state(game_state: GameState) -> None:
        import sys
        from json import dumps

        from RPyG.core_io import CoreIO, input_models, output_models

        save_data = dumps(
            JsonGameStateHandler.serialize_game_state(game_state),
            indent=4,
        ).encode("utf-8")

        with open(JsonGameStateHandler.SAVE_FILE_PATH, "wb") as save_file:
            save_file.write(JsonGameStateHandler.sign_save_file(save_data))  # pyright: ignore[reportUnusedCallResult]

        core_io = CoreIO.get_core_io()
        core_io.send_output(
            output_models.OutputMessage(
                message=f"Successfully Saved Game for {game_state.player_party.name}"
            )
        )

        core_io.request_str_input(
            input_models.UserPromptRequest(
                options=["YES", "NO"],
                prompts=["Would you like to keep playing?"],
            )
        )
        match core_io.receive_str_input():
            case "YES":
                core_io.send_output(
                    output_models.OutputMessage(message="The adventure continues!")
                )
            case "NO":
                sys.exit(0)
            case _:
                raise ValueError("Must be a choice of 'YES' or 'NO'")
