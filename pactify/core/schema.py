from dataclasses import dataclass
from typing import Dict

from pactify.core.field import Field


@dataclass(frozen=True)
class ContractSchema:
    """
    Normalized representation of a contract schema.
    """

    name: str
    version: str | None
    fields: Dict[str, Field]
