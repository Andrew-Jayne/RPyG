from dataclasses import dataclass

from RPyG.core_io.output_models.base_models import OutputMessage


@dataclass(kw_only=True, frozen=True, slots=True)
class GenericStoryMessage(OutputMessage):
    pass
