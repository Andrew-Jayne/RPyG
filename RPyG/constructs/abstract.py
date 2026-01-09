import random
from dataclasses import dataclass


@dataclass
class RandomResultItem[ResultType]:
    result: ResultType
    weight: float


@dataclass
class RandomResultTable[TableResultType]:
    options: list[RandomResultItem[TableResultType]]

    def generate_result(self) -> TableResultType:
        results: list[TableResultType] = list()
        weights: list[float] = list()

        for item in self.options:
            results.append(item.result)
            weights.append(item.weight)

        selection = random.choices(
            results,
            weights=weights,
            k=1,
        )

        return selection[0]
