import pytest

from pactify.core.contract import Contract
from pactify.core.field import Field
from pactify.diff import diff_contracts
from pactify.diff.changes import ChangeSeverity


def make_contract(fields: dict) -> Contract:
    """
    Helper to create contracts quickly.
    """
    return Contract(fields=fields)


def test_no_changes_returns_empty_diff():
    old = make_contract(
        {
            "id": Field(type_="int", required=True),
            "name": Field(type_="string", required=True),
        }
    )

    new = make_contract(
        {
            "id": Field(type_="int", required=True),
            "name": Field(type_="string", required=True),
        }
    )

    result = diff_contracts(old, new)

    assert result.changes == []


def test_add_optional_field_is_safe():
    old = make_contract(
        {
            "id": Field(type_="int", required=True),
        }
    )

    new = make_contract(
        {
            "id": Field(type_="int", required=True),
            "nickname": Field(type_="string", required=False),
        }
    )

    result = diff_contracts(old, new)

    assert len(result.changes) == 1
    change = result.changes[0]

    assert change.path == "nickname"
    assert change.change_type == ChangeSeverity.SAFE


def test_add_required_field_is_breaking():
    old = make_contract(
        {
            "id": Field(type_="int", required=True),
        }
    )

    new = make_contract(
        {
            "id": Field(type_="int", required=True),
            "email": Field(type_="string", required=True),
        }
    )

    result = diff_contracts(old, new)

    assert len(result.changes) == 1
    assert result.changes[0].change_type == ChangeSeverity.BREAKING


def test_remove_field_is_breaking():
    old = make_contract(
        {
            "id": Field(type_="int", required=True),
            "name": Field(type_="string", required=True),
        }
    )

    new = make_contract(
        {
            "id": Field(type_="int", required=True),
        }
    )

    result = diff_contracts(old, new)

    assert len(result.changes) == 1
    assert result.changes[0].path == "name"
    assert result.changes[0].change_type == ChangeSeverity.BREAKING


def test_change_field_type_is_breaking():
    old = make_contract(
        {
            "age": Field(type_="int", required=True),
        }
    )

    new = make_contract(
        {
            "age": Field(type_="string", required=True),
        }
    )

    result = diff_contracts(old, new)

    assert len(result.changes) == 1
    assert result.changes[0].change_type == ChangeSeverity.BREAKING


def test_optional_to_required_is_breaking():
    old = make_contract(
        {
            "phone": Field(type_="string", required=False),
        }
    )

    new = make_contract(
        {
            "phone": Field(type_="string", required=True),
        }
    )

    result = diff_contracts(old, new)

    assert result.changes[0].change_type == ChangeSeverity.BREAKING


def test_required_to_optional_is_safe():
    old = make_contract(
        {
            "phone": Field(type_="string", required=True),
        }
    )

    new = make_contract(
        {
            "phone": Field(type_="string", required=False),
        }
    )

    result = diff_contracts(old, new)

    assert result.changes[0].change_type == ChangeSeverity.SAFE


def test_constraint_change_is_risky():
    old = make_contract(
        {
            "username": Field(type_="string", required=True, max_length=30),
        }
    )

    new = make_contract(
        {
            "username": Field(type_="string", required=True, max_length=20),
        }
    )

    result = diff_contracts(old, new)

    assert result.changes[0].change_type == ChangeSeverity.RISKY
