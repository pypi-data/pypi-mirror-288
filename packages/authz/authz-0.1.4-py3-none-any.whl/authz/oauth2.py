import logging
from typing import Dict, Union, Optional
from pydantic import BaseModel, Field, ConfigDict

from authz.base import Token, AuthZRequestHeaders
from authz.auth import AuthClient, AccountClient


class RequestBody(BaseModel):

    @classmethod
    def create(cls, data: dict, defaults: dict = dict()):
        return cls(**data).assign(defaults)

    def assign(self, defaults: dict = dict()):
        for k, v in defaults.items():
            if not hasattr(self, k):
                continue
            if getattr(self, k, None) is None:
                setattr(self, k, v)
        return self


class TokenRequestBody(RequestBody):
    model_config = ConfigDict(populate_by_name=True)

    code: Optional[str] = Field(default="")
    scope: Optional[str] = Field(default=None)
    grant_type: Optional[str] = Field(default=None)
    client_id: Optional[str] = Field(default=None)
    client_secret: Optional[str] = Field(default=None)
    redirect_uri: Optional[str] = Field(default=None)
    state: Optional[str] = Field(default=None)
    nonce: Optional[str] = Field(default=None)
    account: Optional[str] = Field(default=None)
    password: Optional[str] = Field(default=None)
    refresh_token: Optional[str] = Field(default=None)


class AuthorizeRequestBody(RequestBody):
    model_config = ConfigDict(populate_by_name=True)

    scope: Optional[str] = Field(default=None)
    response_type: Optional[str] = Field(default=None)
    client_id: Optional[str] = Field(default=None)
    client_secret: Optional[str] = Field(default=None)
    redirect_uri: Optional[str] = Field(default=None)
    state: Optional[str] = Field(default=None)
    nonce: Optional[str] = Field(default=None)


class AuthorizeCode(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    code: str


class OAuth2Client(AuthClient, AccountClient):
    """
    The Client class provides a foundation for OAuth 2.0 client operations,
    including authorization, token retrieval, and authentication.
    """

    def authorize(
        self,
        headers_ext: AuthZRequestHeaders,
        payload: Union[Dict[str, str], AuthorizeRequestBody],
    ) -> AuthorizeCode:
        """
        Perform the authorization request to obtain an authorization code.

        :param headers_ext: Extended headers for the authorization request.
        :param payload: A dictionary or AuthorizeRequestBody instance with authorization data.
        :return: An AuthorizeCode instance containing the authorization response.
        """

        url = self.url("/oauth2/authorize")
        defaults = self.default_payload()
        if isinstance(payload, dict):
            payload = AuthorizeRequestBody.create(payload, defaults)
        elif isinstance(payload, AuthorizeRequestBody):
            payload.assign(defaults)
        response = self.client.post(
            url,
            json=payload.model_dump(),
            headers=self.extend_headers(headers_ext),
        )
        response.raise_for_status()
        return AuthorizeCode(**response.json())

    def token(
        self,
        headers_ext: Union[Dict[str, str], AuthZRequestHeaders],
        payload: Union[Dict[str, str], TokenRequestBody],
    ) -> Token:
        """
        Retrieve an access token from the OAuth provider.

        :param headers_ext: Extended headers for the token request.
        :param payload: A dictionary or TokenRequestBody instance with token request data.
        :return: A Token instance containing the token response.
        """
        url = self.url("/oauth2/token")
        defaults = self.default_payload()
        if isinstance(payload, dict):
            payload = AuthorizeRequestBody.create(payload, defaults)
        elif isinstance(payload, TokenRequestBody):
            payload.assign(defaults)
        response = self.client.post(
            url,
            json=payload.model_dump(),
            headers=self.extend_headers(headers_ext),
        )
        response.raise_for_status()
        return Token(**response.json())

    def authenticate(self, headers_ext: AuthZRequestHeaders) -> bool:
        """
        Authenticate a token to verify its validity and permissions.

        :param headers_ext: Extended headers including the authorization token to authenticate.
        :return: True if the token is authenticated successfully, False otherwise.
        """
        url = self.url("/oauth2/authenticate")
        response = self.client.get(url, headers=self.extend_headers(headers_ext))
        response.raise_for_status()
        return True
