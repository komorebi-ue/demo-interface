from __future__ import annotations

from typing import Any
from urllib.parse import urljoin

import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry

from common.logger import log


class RestClient:
    def __init__(self, base_url: str | None = None, default_timeout: int | float = 30):
        self.session = requests.Session()
        self.base_url = (base_url or "").rstrip("/") + "/" if base_url else ""
        self.default_timeout = default_timeout
        self._mount_retry_adapter()

    def _mount_retry_adapter(self) -> None:
        retry = Retry(
            total=3,
            connect=3,
            read=3,
            backoff_factor=0.5,
            status_forcelist=(429, 500, 502, 503, 504),
            allowed_methods=("GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS", "HEAD"),
            raise_on_status=False,
        )
        adapter = HTTPAdapter(max_retries=retry)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

    def request(
        self,
        method: str,
        url: str,
        *,
        params: dict[str, Any] | None = None,
        data: Any | None = None,
        json: Any | None = None,
        headers: dict[str, str] | None = None,
        timeout: int | float | None = None,
        **kwargs: Any,
    ) -> requests.Response:
        full_url = urljoin(self.base_url, url.lstrip("/")) if self.base_url else url
        used_timeout = timeout if timeout is not None else self.default_timeout
        log.info(
            "Request -> {method} {url} | params={params}",
            method=method.upper(),
            url=full_url,
            params=params,
        )
        resp = self.session.request(
            method=method,
            url=full_url,
            params=params,
            data=data,
            json=json,
            headers=headers,
            timeout=used_timeout,
            **kwargs,
        )
        if resp.status_code >= 400:
            snippet = (resp.text or "")[:300].replace("\n", " ").replace("\r", " ")
            log.error(
                "HTTP error <- {method} {url} | status={status_code} | body={body}",
                method=method.upper(),
                url=full_url,
                status_code=resp.status_code,
                body=snippet,
            )
        log.info(
            "Response <- {method} {url} | status={status_code}",
            method=method.upper(),
            url=full_url,
            status_code=resp.status_code,
        )
        return resp

