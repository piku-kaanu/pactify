from pactify.core.schema import ContractSchema
from pactify.diff.changes import Change
from pactify.diff.rules import CompatibilityRules


def diff_contracts(
    old: ContractSchema,
    new: ContractSchema,
) -> list[Change]:
    """
    Compare two contract schemas and return a list of changes.
    """
    changes: list[Change] = []

    # Field removed
    for field in old.fields:
        if field not in new.fields:
            changes.append(
                CompatibilityRules.classify(
                    kind="FIELD_REMOVED",
                    field=field,
                    message=f"Field '{field}' was removed",
                )
            )

    # Field added
    for field in new.fields:
        if field not in old.fields:
            changes.append(
                CompatibilityRules.classify(
                    kind="FIELD_ADDED",
                    field=field,
                    message=f"Field '{field}' was added",
                )
            )

    return changes
