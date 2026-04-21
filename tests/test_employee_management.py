from __future__ import annotations

import random
import string
from pathlib import Path

import pytest
import yaml


def _load_employee_data() -> dict:
    p = Path(__file__).parent.parent / "data" / "employee_data.yaml"
    with p.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


@pytest.fixture()
def created_employee(employee_api):
    """
    Create employee for test, always delete afterwards.
    Yields: dict with keys: emp_number, first_name, last_name, employee_id
    """
    data = _load_employee_data().get("employees", {})
    first = random.choice(data.get("first_names", ["Auto"]))
    last = random.choice(data.get("last_names", ["Employee"]))
    suffix = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
    first_name = f"{first}{suffix}"
    last_name = f"{last}{suffix}"
    employee_id = "".join(random.choices(string.digits, k=6))

    resp = employee_api.add_employee(first_name=first_name, last_name=last_name, emp_id=employee_id)
    emp_number = (resp.get("data") or {}).get("empNumber")

    if not emp_number:
        raise AssertionError(f"Add employee succeeded but empNumber missing: {resp}")

    yield {
        "emp_number": int(emp_number),
        "first_name": first_name,
        "last_name": last_name,
        "employee_id": employee_id,
    }

    employee_api.delete_employee(int(emp_number))


def test_employee_add_list_delete(employee_api, created_employee):
    created = created_employee

    # list may be paged; try a few pages
    found = False
    for offset in (0, 50, 100, 150):
        employees = employee_api.get_employee_list(limit=50, offset=offset)
        items = (employees.get("data") or [])
        for e in items:
            if e.get("empNumber") == created["emp_number"]:
                found = True
                break
        if found:
            break

    assert found, f"Employee not found in list, empNumber={created['emp_number']}"

