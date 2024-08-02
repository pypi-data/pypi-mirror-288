from __future__ import annotations

import typing

import requests
import requests.auth

from .exceptions import AuthError

DEFAULT_TIMEOUT = 300

__all__ = ["TouchpointClientAuth"]


class TouchpointClientAuth(requests.auth.AuthBase):

    _authorization: typing.Optional[str] = None
    _authorization_params: typing.Optional[str] = None
    _auth_url: str
    _scope: set

    def __init__(
        self,
        client_id,
        auth_url,
        *,
        username=None,
        password=None,
        client_secret=None,
        timeout=DEFAULT_TIMEOUT,
    ):
        self._auth_url = auth_url
        self._client_id = client_id
        self._client_secret = client_secret
        self._timeout = timeout
        if username and password:
            self.authenticate_password(username, password)
        else:
            raise AuthError(404, "Missing username or password")

    def __call__(self, r):
        r.headers["Authorization"] = self._authorization
        return r

    def authenticate_password(self, username, password):
        self._authorization_params = {
            "username": username,
            "password": password,
            "client_id": self._client_id,
            "grant_type": "password",
            "error_details": True,
            "client_secret": self._client_secret,
        }
        self.invalidate()

    def invalidate(self):
        self._authorization = None
        self.authenticate()

    def authenticate(self):
        res = requests.post(
            self._auth_url,
            params=self._authorization_params,
            verify=False,
            timeout=self._timeout,
        )
        if res.status_code == 200:
            js = res.json()
            self._authorization = f"""{js["token_type"].capitalize()} {js["access_token"]}"""
            self._scope = set(js["scope"].split(" "))
        else:
            raise AuthError(res.status_code, res.text)

    @property
    def scope(self):
        return self._scope
