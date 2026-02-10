from dataclasses import dataclass
from typing import Dict

from pactify.core.field import Field
from pactify.core.schema import ContractSchema


@dataclass(frozen=True)
class Contract:
    """
    Runtime representation of a contract.

    The tests construct contracts directly as:

        Contract(fields={...})

    and then pass them to ``diff_contracts``.  This lightweight data
    container supports that usage while also exposing a ``schema()``
    helper that normalises the instance into a ``ContractSchema``.
    """

    fields: Dict[str, Field]
    name: str = "Contract"
    version: str | None = None

    def schema(self) -> ContractSchema:
        return ContractSchema(
            name=self.name,
            version=self.version,
            fields=self.fields,
        )
