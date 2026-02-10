from pactify.diff.changes import ChangeSeverity


def classify_change(change: ChangeSeverity) -> ChangeSeverity:
    """
    Determine severity of a single schema change.
    """
    kind = change.kind
    details = change.details

    if kind == "field_added":
        return ChangeSeverity.SAFE if details["required"] is False else ChangeSeverity.BREAKING

    if kind == "field_removed":
        return ChangeSeverity.BREAKING

    if kind == "type_changed":
        return ChangeSeverity.BREAKING

    if kind == "required_changed":
        if details["from"] is True and details["to"] is False:
            return ChangeSeverity.SAFE
        return ChangeSeverity.BREAKING

    if kind == "constraint_changed":
        if details["narrowed"] is True:
            return ChangeSeverity.RISKY
        return ChangeSeverity.SAFE

    return ChangeSeverity.RISKY  # conservative default
