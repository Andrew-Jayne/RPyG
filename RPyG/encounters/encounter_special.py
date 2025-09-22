# Just for Type Checking
from RPyG.actors import PlayerParty
from RPyG.core_io import CoreIO
from RPyG.core_io.io_models import OutputMessage, UserPromptRequest
from RPyG.utilites import ensure_type


# TODO, make this not a pile of static method, or otherwise de-stupid-ify this module


class SpecialEncounters:
    @staticmethod
    def tavern_notice(player_party_instance: PlayerParty) -> None:
        ensure_type(player_party_instance, PlayerParty, "player_party_instance")
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
