from pactify.diff.severity import classify_change
from pactify.diff.changes import ChangeSeverity
from pactify.diff.changes import Change


def test_narrowing_constraint_is_risky():
    change = Change(
        path="username",
        kind="constraint_changed",
        details={
            "constraint": "max_length",
            "from": 30,
            "to": 20,
            "narrowed": True,
        },
    )

    assert classify_change(change) == ChangeSeverity.RISKY
