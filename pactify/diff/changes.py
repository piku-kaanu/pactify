from dataclasses import dataclass
from enum import Enum


class ChangeSeverity(str, Enum):
    SAFE = "SAFE"
    RISKY = "RISKY"
    BREAKING = "BREAKING"


@dataclass(frozen=True)
class Change:
    kind: str
    field: str | None
    severity: ChangeSeverity
    message: str
