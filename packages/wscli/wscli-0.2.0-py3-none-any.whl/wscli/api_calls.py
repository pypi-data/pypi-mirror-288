"""standard api call methods"""

import logging
from dataclasses import dataclass
from enum import Enum
from typing import Dict

import requests

logger = logging.getLogger(__name__)


class Scheme(Enum):
    HTTP = "http"
    HTTPS = "https"


class Method(Enum):
    GET = "get"
    POST = "post"


class ContentType(Enum):
    HTML = "text/html"
    JSON = "application/json"


@dataclass(kw_only=True)
class ApiUrl:
    domain: str = "localhost"
    scheme: Scheme = Scheme.HTTP
    port: int = 8000
    base_route: str = ""

    def url(self, endpoint: str = ""):
        base_route = self.base_route.lstrip("/")
        route = f"{base_route}/{endpoint.strip('/')}"
        return f"{self.scheme.value}://{self.domain}:{self.port}/{route}"


@dataclass(kw_only=True)
class CallConfig:
    token: str | None = None
    method: Method = Method.GET
    content_type: ContentType | None = None

    @property
    def headers(self) -> Dict[str, str]:
        headers: Dict[str, str] = {}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        if self.content_type:
            headers["Content-type"] = str(self.content_type.value)
        return headers


def hit_api(
    endpoint: str,
    api_url: ApiUrl,
    call_config: CallConfig | None = None,
    payload: dict | None = None,
):
    call_config = call_config or CallConfig()
    url = api_url.url(endpoint)
    method = call_config.method.value

    logger.warning(
        f"making request {call_config.method.name} to endpoint {url}"
    )
    response = requests.request(
        method, url, headers=call_config.headers, json=payload
    )
    return response
