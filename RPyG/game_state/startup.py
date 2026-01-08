import os

from RPyG.actors import PlayableActor, PlayerParty
from RPyG.core_io import CoreIO
from RPyG.core_io.io_models import CustomTextRequest, OutputMessage, UserPromptRequest
from RPyG.exceptions import ImpossibleValueException
from RPyG.game_state.file import load_game
from RPyG.utilities import setup_logger


logger = setup_logger(__name__)


def default_party() -> PlayerParty:
    party_members: list[PlayableActor] = []
    default_names = ("Conan", "Merlin", "Robin")
    default_specialization = ("WARRIOR", "MAGE", "ROGUE")
    for i in range(0, 3):
        party_members.append(
            PlayableActor(
                default_names[i],
                default_specialization[i],
            )
        )

    return PlayerParty(
        members=party_members,
        name="The Default Party",
    )


def get_start_type() -> str:
    if os.path.exists("use_default.flag") is True:
        return "USE_DEFAULT"
    match os.path.exists("savegame.rpygs"):
        case True:
            start_game_options = ["NEW", "LOAD"]
            start_game_messages = [
                "Would you like to Start a new game or Load an existing save?",
                "Options are:",
            ]
        case False:
            start_game_options = ["NEW"]
            start_game_messages = [
                "Type 'NEW' to start a new game",
                "You will be able to save your game later and load it here",
                "Options are:",
            ]
        case _:  # pyright: ignore[reportUnnecessaryComparison]
            raise ImpossibleValueException(  # pyright: ignore[reportUnreachable]
                "os.path.exists('savegame.rpygs') did not return a bool and something is very wrong"
            )

    core_io = CoreIO.get_core_io()
    core_io.send_output(OutputMessage("Welcome to RPyG, a text based RPG in Python"))
    core_io.request_input(
        UserPromptRequest(
            options=start_game_options,
            prompts=start_game_messages,
        )
    )
    player_action = core_io.receive_input()
    return player_action


def party_start() -> PlayerParty:
    party_size_choices = ["1", "2", "3"]
    party_size_messages = ["How many members are in your party?"]

    specialization_choices = ["WARRIOR", "MAGE", "ROGUE"]
    specialization_messages = ["What Specialization will this member use?"]

    member_name_messages = [
        "Before their journey can begin you must name your Character",
        "NOTE: Case is respected but names longer than 32 characters will be truncated",
    ]

    party_name_messages = [
        "Before their journey can begin you must name your Party",
        "NOTE: Case is respected but names longer than 64 characters will be truncated",
    ]
    core_io = CoreIO.get_core_io()

    core_io.request_input(
        UserPromptRequest(
            options=party_size_choices,
            prompts=party_size_messages,
        )
    )
    party_size = int(core_io.receive_input())

    party_instances: list[PlayableActor] = []
    for _ in range(0, party_size):
        core_io = CoreIO.get_core_io()
        core_io.request_input(
            CustomTextRequest(
                prompts=member_name_messages,
                max_length=32,
            )
        )
        member_name = core_io.receive_input()
        core_io.request_input(
            UserPromptRequest(
                prompts=specialization_messages,
                options=specialization_choices,
            )
        )
        member_specialization = core_io.receive_input()
        member = PlayableActor(member_name, member_specialization)
        party_instances.append(member)

    core_io.request_input(
        CustomTextRequest(
            prompts=party_name_messages,
            max_length=64,
        )
    )
    party_name = core_io.receive_input()

    return PlayerParty(party_name, party_instances)


def get_player_party_instance() -> PlayerParty:
    # Get Player Party Instance from file or create a new one
    logger.info("Getting Start type")
    start_type = get_start_type()
    match start_type:
        case "LOAD":
            player_party_instance = load_game()
        case "NEW":
            player_party_instance = party_start()
        case "USE_DEFAULT":
            player_party_instance = default_party()
        case _:
            raise ValueError("Invalid Game Start Type")

    logger.info("starting game with %s start type", start_type)

    return player_party_instance
