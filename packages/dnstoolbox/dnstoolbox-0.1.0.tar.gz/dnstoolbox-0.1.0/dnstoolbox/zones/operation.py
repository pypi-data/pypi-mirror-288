from dataclasses import dataclass
from enum import Enum

from dnstoolbox.records import Record


class OperationType(str, Enum):
    CREATE = "create"
    DELETE = "delete"


@dataclass
class Operation:
    domain: str
    record: Record
    type: OperationType

    @classmethod
    def from_tuple(cls, t):
        return Operation(*t)

    def totuple(self):
        return (self.domain, self.record, self.type)

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Operation):
            raise NotImplementedError(
                f"Comparison is not implemented between {type(self)} and {type(value)}"
            )
        return self.totuple() == value.totuple()

    def __hash__(self) -> int:
        return hash(self.totuple())


__all__ = [
    "OperationType",
    "Operation",
]
