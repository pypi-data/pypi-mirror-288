from __future__ import annotations

import typing
from urllib.parse import urljoin

import requests

from ._auth import TouchpointClientAuth
from .exceptions import AccessDeniedError, AuthError, RequestError, ServerError
from .types import ConnectorBase

DEFAULT_TIMEOUT = 300

__all__ = ["Connector"]


class Connector(ConnectorBase):

    _auth: typing.Optional[TouchpointClientAuth]
    _authorization: typing.Optional[str] = None
    _authorization_params: typing.Optional[dict] = None

    def __init__(
        self,
        api_url,
        auth: typing.Optional[TouchpointClientAuth] = None,
        timeout=DEFAULT_TIMEOUT,
    ):
        self.api_url = api_url
        self._timeout = timeout
        self._auth = auth
        self.session = requests.Session()
        self.session.auth = auth

    def url(self, part):
        return urljoin(self.api_url, part)

    def _head(self, **kwargs):
        head = {
            "timeout": self._timeout,
            "verify": False,
        }
        head.update(kwargs)
        return head

    def head(self, uri: str, **kwargs):
        kwargs = self._head(**kwargs)
        return self.request("HEAD", uri, **kwargs)

    def get(self, uri: str, **kwargs):
        kwargs = self._head(**kwargs)
        return self.request("GET", uri, **kwargs)

    def post(self, uri: str, **kwargs):
        kwargs = self._head(**kwargs)
        return self.request("POST", uri, **kwargs)

    def put(self, uri: str, **kwargs):
        kwargs = self._head(**kwargs)
        return self.request("PUT", uri, **kwargs)

    def patch(self, uri: str, **kwargs):
        kwargs = self._head(**kwargs)
        return self.request("PATCH", uri, **kwargs)

    def delete(self, uri: str, **kwargs):
        kwargs = self._head(**kwargs)
        return self.request("DELETE", uri, **kwargs)

    def request(self, method: str, uri: str, **kwargs):
        url = self.url(uri)
        response = self.session.request(method, url, **kwargs)
        if response.status_code == 401:
            self.invalidate()
            response = self.session.request(method, url, **kwargs)
        if response.status_code == 401:
            raise AuthError(response.status_code, response.text)
        if response.status_code == 403:
            raise AccessDeniedError(response.status_code, response.text)
        if 300 <= response.status_code <= 400:
            raise RequestError(response.status_code, response.text)
        if 500 <= response.status_code < 600:
            raise ServerError(response.status_code, response.text)
        return response

    def invalidate(self):
        if self._auth:
            self._auth.invalidate()
