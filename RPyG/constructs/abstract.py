import random
from collections.abc import Generator
from contextlib import contextmanager
from dataclasses import dataclass

from RPyG.utilities import ensure_type


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


class BorrowTrackedResource[InstanceType]:
    _resource: InstanceType | None
    _borrow_count: int
    _resource_type: type[InstanceType]

    def __init__(self, resource_type: type[InstanceType]) -> None:
        self._resource = None
        self._borrow_count = 0
        self._resource_type = resource_type

    @property
    def resource_type(self) -> type[InstanceType]:
        return self._resource_type

    def load_resource(self, resource_instance: InstanceType) -> None:
        ensure_type(resource_instance, self.resource_type, "resource_instance")
        if self._resource is not None:
            raise RuntimeError(
                "Cannot load resource, an active instance is present, use destroy_resource() to remove the current instance"
            )
        self._resource = resource_instance

    @contextmanager
    def borrow_resource(self) -> Generator[InstanceType]:
        if self._resource is None:
            raise RuntimeError(
                "No loaded resource for borrowing, use load_resource() to add a resource"
            )
        self._borrow_count += 1
        try:
            yield self._resource
        finally:
            self._borrow_count -= 1

    def destroy_resource(self) -> None:
        if self._borrow_count == 0:
            self._resource = None
        else:
            raise RuntimeError(
                f"Cannot destroy resource, borrow count is {self._borrow_count} and must be 0"
            )
