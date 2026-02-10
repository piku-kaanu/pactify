from pactify.core.field import Field
from pactify.diff.changes import Change, ChangeSeverity


class CompatibilityRules:
    """
    Encapsulates compatibility rules for schema changes.

    These rules intentionally mirror the expectations encoded in the
    tests under ``tests/diff/test_diff_contracts.py``.
    """

    @staticmethod
    def _is_required(field: Field) -> bool:
        """
        Determine whether a field is required.

        The public ``Field`` API stores arbitrary keyword arguments in
        ``constraints``; the tests use ``required=...`` there.
        """

        return bool(field.constraints.get("required", False))

    @staticmethod
    def _constraints_without_required(field: Field) -> dict:
        return {
            key: value
            for key, value in field.constraints.items()
            if key != "required"
        }

    @classmethod
    def added_field(cls, name: str, field: Field) -> Change:
        """
        Classify the addition of a field.

        - Adding an *optional* field is SAFE
        - Adding a *required* field is BREAKING
        """

        required = cls._is_required(field)
        severity = ChangeSeverity.BREAKING if required else ChangeSeverity.SAFE
        message = (
            f"Required field '{name}' was added"
            if required
            else f"Optional field '{name}' was added"
        )
        return Change(path=name, change_type=severity, message=message)

    @classmethod
    def removed_field(cls, name: str, field: Field) -> Change:
        """
        Removing a field is always BREAKING.
        """

        return Change(
            path=name,
            change_type=ChangeSeverity.BREAKING,
            message=f"Field '{name}' was removed",
        )

    @classmethod
    def modified_field(cls, name: str, old: Field, new: Field) -> Change | None:
        """
        Classify a change to an existing field.

        - Changing the type is BREAKING
        - Optional -> required is BREAKING
        - Required -> optional is SAFE
        - Any other constraint change is RISKY
        - No effective change returns ``None``
        """

        if old.type != new.type:
            return Change(
                path=name,
                change_type=ChangeSeverity.BREAKING,
                message=(
                    f"Field '{name}' type changed from {old.type!r} "
                    f"to {new.type!r}"
                ),
            )

        old_required = cls._is_required(old)
        new_required = cls._is_required(new)

        if old_required != new_required:
            if (not old_required) and new_required:
                severity = ChangeSeverity.BREAKING
                description = "optional to required"
            else:
                severity = ChangeSeverity.SAFE
                description = "required to optional"

            return Change(
                path=name,
                change_type=severity,
                message=f"Field '{name}' changed from {description}",
            )

        old_constraints = cls._constraints_without_required(old)
        new_constraints = cls._constraints_without_required(new)

        if old_constraints != new_constraints:
            return Change(
                path=name,
                change_type=ChangeSeverity.RISKY,
                message=f"Constraints for field '{name}' changed",
            )

        # No meaningful change detected
        return None
