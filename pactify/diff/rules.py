from pactify.diff.changes import Change, ChangeSeverity


class CompatibilityRules:
    """
    Encapsulates compatibility rules for schema changes.
    """

    @staticmethod
    def classify(*, kind: str, field: str | None, message: str) -> Change:
        """
        Placeholder rule classifier.
        """
        return Change(
            kind=kind,
            field=field,
            severity=ChangeSeverity.RISKY,
            message=message,
        )
