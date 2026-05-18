from RPyG.utilities import ensure_type


class Inventory:
    gold: int
    potions: int
    actor_name: str
    __slots__: tuple[str, ...] = ("gold", "potions", "actor_name")

    def __init__(
        self,
        gold: int,
        potions: int,
        actor_name: str,
    ) -> None:
        ensure_type(gold, int, "gold")
        ensure_type(potions, int, "potions")
        ensure_type(actor_name, str, "actor_name")

        self.actor_name = actor_name
        self.gold = gold
        self.potions = potions

    def gain_gold(self, amount: int) -> None:
        self.gold += amount

    def spend_gold(self, amount: int) -> bool:
        from RPyG.core_io import CoreIO, output_models

        core_io = CoreIO.get_core_io()

        if self.gold < amount:
            core_io.send_output(
                output_models.OutputMessage(f"{self.actor_name} has insufficient gold")
            )
            return False
        else:
            Inventory.lose_gold(self, amount)
            return True

    def lose_gold(self, amount: int) -> None:
        from RPyG.core_io import CoreIO, output_models

        core_io = CoreIO.get_core_io()

        self.gold -= amount
        if self.gold < 0:
            self.gold = 0
            core_io.send_output(
                output_models.OutputMessage(f"{self.actor_name} has no gold remaining")
            )

    def gain_potion(self, amount: int) -> None:
        self.potions += amount

    def lose_potion(self, amount: int) -> None:
        self.potions -= amount
        if self.potions < 0:
            self.potions = 0
