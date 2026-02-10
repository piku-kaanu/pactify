from pactify.core.contract import Contract
from pactify.core.schema import ContractSchema
from pactify.diff.changes import DiffResult
from pactify.diff.rules import CompatibilityRules


def _to_schema(contract_or_schema: ContractSchema | Contract) -> ContractSchema:
    """
    Normalise either a ``Contract`` instance or an already constructed
    ``ContractSchema`` into a ``ContractSchema``.
    """

    if isinstance(contract_or_schema, ContractSchema):
        return contract_or_schema

    if isinstance(contract_or_schema, Contract):
        return contract_or_schema.schema()

    # Be forgiving: if it quacks like a Contract and exposes ``schema()``,
    # use that as well.  This keeps the function flexible for callers.
    if hasattr(contract_or_schema, "schema"):
        return contract_or_schema.schema()

    raise TypeError(
        "diff_contracts expects Contract or ContractSchema instances, "
        f"got {type(contract_or_schema)!r}"
    )


def diff_contracts(
    old: ContractSchema | Contract,
    new: ContractSchema | Contract,
) -> DiffResult:
    """
    Compare two contracts and return a ``DiffResult``.

    The public tests construct simple ``Contract`` instances that wrap
    a mapping of field names to ``Field`` objects.  This function
    supports both those and pre‑built ``ContractSchema`` objects.
    """

    old_schema = _to_schema(old)
    new_schema = _to_schema(new)

    changes = []

    # Field removed
    for name, field in old_schema.fields.items():
        if name not in new_schema.fields:
            changes.append(CompatibilityRules.removed_field(name, field))

    # Field added
    for name, field in new_schema.fields.items():
        if name not in old_schema.fields:
            changes.append(CompatibilityRules.added_field(name, field))

    # Field modified
    for name, old_field in old_schema.fields.items():
        if name in new_schema.fields:
            new_field = new_schema.fields[name]
            change = CompatibilityRules.modified_field(name, old_field, new_field)
            if change is not None:
                changes.append(change)

    return DiffResult(changes=changes)
