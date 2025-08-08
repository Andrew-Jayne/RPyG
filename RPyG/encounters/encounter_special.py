# Just for Type Checking
from RPyG.actors import EnemyParty, PlayerParty
from RPyG.combat import battle
from RPyG.content import ContentLibrary
from RPyG.core_io import CoreIO
from RPyG.core_io.io_models import OutputMessage, UserPromptRequest
from RPyG.encounters.encounter_dungeon import Dungeon
from RPyG.gameState.file import save_game
from RPyG.utilites import ensure_type


# TODO, make this not a pile of static method, or otherwise de-stupid-ify this module


class SpecialEncounters:
    @staticmethod
    def send_special_encounter_message(
        progress_value,
        party_name,
        message_type,
    ) -> None:
        core_io = CoreIO.get_core_io()
        content_library = ContentLibrary.get_library()

        all_events = content_library.story_events

        current_event = all_events[progress_value]
        match message_type:
            case "messages":
                active_messages = current_event.messages
            case "success_messages":
                active_messages = current_event.success_messages
            case "failure_messages":
                active_messages = current_event.failure_messages
            case _:
                raise ValueError(
                    'Message type must be one of ["messages", "success_messages", "failure_messages"]'
                )
        for message in active_messages:
            core_io.send_output(OutputMessage(message.format(party_name=party_name)))

    @staticmethod
    def tavern_notice(player_party_instance: PlayerParty) -> None:
        ensure_type(player_party_instance, PlayerParty, 'player_party_instance')
        core_io = CoreIO.get_core_io()

        SpecialEncounters.send_special_encounter_message(
            player_party_instance.progress,
            player_party_instance.name,
            "messages",
        )

        embark_options = ["EMBARK", "DRINK"]
        embark_options_message = ["What shall the party do?"]
        core_io.request_input(
            UserPromptRequest(
                options=embark_options,
                prompts=embark_options_message,
            )
        )
        player_choice = core_io.receive_input()

        while player_choice != "EMBARK":
            core_io.request_input(
                UserPromptRequest(
                    options=embark_options,
                    prompts=embark_options_message,
                )
            )
            player_choice = core_io.receive_input()

            match player_choice:
                case "EMBARK":
                    return
                case "DRINK":
                    ## TODO Hard Coded text, needs to be moved to some other system
                    core_io.send_output(
                        OutputMessage(
                            "After many drinks, the kings missive sticks in your minds.",
                        )
                    )
                case _:
                    return

    @staticmethod
    def friendly_keep_visit(player_party_instance: PlayerParty) -> None:
        ensure_type(player_party_instance, PlayerParty, "player_party_instance")
        core_io = CoreIO.get_core_io()

        ## TODO Hard Coded text, needs to be moved to some other system
        core_io.send_output(
            OutputMessage(
                f"{player_party_instance.name} is welcomed at the Open Hall by King Stallman"
            )
        )
        SpecialEncounters.send_special_encounter_message(
            player_party_instance.progress,
            player_party_instance.name,
            "messages",
        )

        quest_options = ["ACCEPT", "DECLINE"]
        quest_message = ["Will you accept this quest from the King?"]
        core_io.request_input(
            UserPromptRequest(
                options=quest_options,
                prompts=quest_message,
            )
        )
        player_choice = core_io.receive_input()

        while player_choice != "ACCEPT":
            core_io.request_input(
                UserPromptRequest(
                    options=quest_options,
                    prompts=quest_message,
                )
            )
            player_choice = core_io.receive_input()
            match player_choice:
                case "ACCEPT":
                    pass
                case "DECLINE":
                    core_io.send_output(
                        OutputMessage("The King insists, and asks again")
                    )
                case _:
                    pass
        for member_instance in player_party_instance.members:
            member_instance.heal(300)
            member_instance.inventory.gain_potion(9)

        core_io.send_output(
            OutputMessage(
                f"{player_party_instance.name} is are fully rested and have a full stock of potions"
            )
        )

    @staticmethod
    def midway_boss(player_party_instance: PlayerParty) -> None:
        ensure_type(player_party_instance, PlayerParty, "player_party_instance")
        content_library = ContentLibrary.get_library()

        enemy_instance = content_library.special_enemies["midway_boss"]

        SpecialEncounters.send_special_encounter_message(
            player_party_instance.progress,
            player_party_instance.name,
            "messages",
        )

        enemy_party = EnemyParty(enemy_instance.name, [enemy_instance])
        battle(player_party_instance, enemy_party)
        if len(player_party_instance.members) != 0:
            SpecialEncounters.send_special_encounter_message(
                player_party_instance.progress,
                player_party_instance.name,
                "success_messages",
            )
        else:
            SpecialEncounters.send_special_encounter_message(
                player_party_instance.progress,
                player_party_instance.name,
                "failure_messages",
            )

    @staticmethod
    def enemy_keep_visit(player_party_instance: PlayerParty) -> None:
        content_library = ContentLibrary.get_library()
        SpecialEncounters.send_special_encounter_message(
            player_party_instance.progress,
            player_party_instance.name,
            "messages",
        )

        if "algolons_fortress" not in content_library.special_dungeons.keys():
            raise FileNotFoundError(
                f"Unable to locate Dungeon with the ID algolons_fortress, avalible IDs are {content_library.special_dungeons.keys()}"
            )
        active_dungeon: Dungeon = content_library.special_dungeons["algolons_fortress"]
        active_dungeon.travese_dungeon(player_party_instance)

    @staticmethod
    def penultimate_boss(player_party_instance: PlayerParty) -> None:
        ensure_type(player_party_instance, PlayerParty, "player_party_instance")
        core_io = CoreIO.get_core_io()
        content_library = ContentLibrary.get_library()

        enemy_instance = content_library.special_enemies["penultimate_boss"]
        core_io.send_output(OutputMessage(f"Your Party Battles {enemy_instance.name}!"))
        enemy_party = EnemyParty(enemy_instance.name, [enemy_instance])
        battle(player_party_instance, enemy_party)
        if len(player_party_instance.members) != 0:
            SpecialEncounters.send_special_encounter_message(
                player_party_instance.progress,
                player_party_instance.name,
                "success_messages",
            )
        else:
            SpecialEncounters.send_special_encounter_message(
                player_party_instance.progress,
                player_party_instance.name,
                "failure_messages",
            )

    @staticmethod
    def final_boss(player_party_instance: PlayerParty) -> None:
        ensure_type(player_party_instance, PlayerParty, "player_party_instance")
        core_io = CoreIO.get_core_io()
        content_library = ContentLibrary.get_library()

        enemy_instance = content_library.special_enemies["ultimate_boss"]

        core_io.send_output(
            OutputMessage(f"Your Party must now battle {enemy_instance.name}!")
        )
        enemy_party = EnemyParty(enemy_instance.name, [enemy_instance])
        battle(player_party_instance, enemy_party)
        if len(player_party_instance.members) != 0:
            SpecialEncounters.send_special_encounter_message(
                player_party_instance.progress,
                player_party_instance.name,
                "success_messages",
            )
            core_io.send_output(
                OutputMessage(f"""
    Fortranus the Ancient One has been Vanquished at the hands of {player_party_instance.name}


    Your adventure has been completed, you may start a new adventure if you so choose
    """)
            )
            save_game(player_party_instance)
        else:
            SpecialEncounters.send_special_encounter_message(
                player_party_instance.progress,
                player_party_instance.name,
                "failure_messages",
            )
