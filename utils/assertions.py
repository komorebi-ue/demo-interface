from __future__ import annotations

from typing import Any


def assert_status_code(actual: int, expected: int | tuple[int, ...]) -> None:
    if isinstance(expected, tuple):
        assert actual in expected, f"Expected status in {expected}, got {actual}"
    else:
        assert actual == expected, f"Expected status {expected}, got {actual}"


def assert_has_keys(payload: dict[str, Any], required_keys: list[str]) -> None:
    missing = [k for k in required_keys if k not in payload]
    assert not missing, f"Missing keys in payload: {missing}. Payload keys: {list(payload.keys())}"


def assert_employee_create_response(payload: dict[str, Any]) -> int:
    """
    Validate key fields in create-employee response and return empNumber.
    """
    assert_has_keys(payload, ["data"])
    data = payload.get("data") or {}
    assert isinstance(data, dict), f"`data` should be dict, got {type(data)}"
    assert_has_keys(data, ["empNumber"])
    emp_number = data["empNumber"]
    assert isinstance(emp_number, int), f"`empNumber` should be int, got {type(emp_number)}"
    return emp_number

