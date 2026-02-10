from dataclasses import dataclass
from enum import Enum


class ChangeSeverity(str, Enum):
    SAFE = "SAFE"
    RISKY = "RISKY"
    BREAKING = "BREAKING"


@dataclass(frozen=True)
class Change:
    """
    Describes a single compatibility change detected between two contracts.

    The tests access ``path`` and ``change_type`` only, but ``message`` is
    included to provide a human‑readable explanation when needed.
    """

    path: str
    change_type: ChangeSeverity
    message: str


@dataclass(frozen=True)
class DiffResult:
    """
    Container returned by ``diff_contracts``.

    It simply wraps the list of individual changes.
    """

    changes: list[Change]
