from __future__ import annotations

from typing import Any

import requests

from common.logger import log


class RestClient:
    def __init__(self):
        self.session = requests.Session()

    def request(
        self,
        method: str,
        url: str,
        *,
        params: dict[str, Any] | None = None,
        data: Any | None = None,
        json: Any | None = None,
        headers: dict[str, str] | None = None,
        timeout: int | float = 30,
        **kwargs: Any,
    ) -> requests.Response:
        log.info(
            "Request -> {method} {url} | params={params}",
            method=method.upper(),
            url=url,
            params=params,
        )
        resp = self.session.request(
            method=method,
            url=url,
            params=params,
            data=data,
            json=json,
            headers=headers,
            timeout=timeout,
            **kwargs,
        )
        log.info(
            "Response <- {method} {url} | status={status_code}",
            method=method.upper(),
            url=url,
            status_code=resp.status_code,
        )
        return resp

