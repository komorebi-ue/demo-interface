from __future__ import annotations

from typing import Any

from common.rest_client import RestClient


class EmployeeApi:
    """
    OrangeHRM Employee API wrapper.

    Base endpoint:
      /web/index.php/api/v2/pim/employees
    """

    def __init__(self, client: RestClient, base_url: str):
        self.client = client
        self.base_url = base_url.rstrip("/") + "/"
        self._employees_path = "/web/index.php/api/v2/pim/employees"

    @property
    def _default_headers(self) -> dict[str, str]:
        return {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "X-Requested-With": "XMLHttpRequest",
        }

    def add_employee(self, first_name: str, last_name: str, emp_id: str | None = None) -> dict[str, Any]:
        payload: dict[str, Any] = {"firstName": first_name, "lastName": last_name}
        if emp_id:
            payload["employeeId"] = emp_id

        resp = self.client.request(
            "POST",
            self._employees_path,
            json=payload,
            headers=self._default_headers,
        )
        resp.raise_for_status()
        return resp.json()

    def get_employee_list(self, *, limit: int = 50, offset: int = 0, model: str = "default") -> dict[str, Any]:
        resp = self.client.request(
            "GET",
            self._employees_path,
            params={"limit": limit, "offset": offset, "model": model},
            headers=self._default_headers,
        )
        resp.raise_for_status()
        return resp.json()

    def delete_employee(self, emp_number: int) -> dict[str, Any]:
        """
        API expects a list of ids, we wrap single delete.
        """
        resp = self.client.request(
            "DELETE",
            self._employees_path,
            json={"ids": [emp_number]},
            headers=self._default_headers,
        )
        resp.raise_for_status()
        return resp.json()

