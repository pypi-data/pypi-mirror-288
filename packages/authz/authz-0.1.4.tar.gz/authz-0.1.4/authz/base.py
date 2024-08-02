import httpx
from urllib.parse import urljoin
from typing import Dict, Optional, Union

from enum import Enum
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class Token(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id_token: Optional[str] = Field(default=None)
    access_token: str
    refresh_token: str
    expires_at: Optional[datetime] = Field(default=None)
    token_type: str


class AuthorizationHeaderType(str, Enum):

    model_config = ConfigDict(populate_by_name=True)

    BASIC = "Basic"
    BEARER = "Bearer"


class AuthorizationHeader(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    token: str
    token_type: AuthorizationHeaderType

    def to_str(self) -> str:
        return f"{self.token_type.value} {self.token}"

    def to_dict(self) -> dict:
        return {"authorization": f"{self.token_type.value} {self.token}"}


class AuthZRequestHeaders(BaseModel):
    PREFIX: str = "x-authz"

    model_config = ConfigDict(populate_by_name=True)

    appid: str
    port: str
    host: str
    resource: str
    method: str
    authorization: AuthorizationHeader

    def to_dict(self):
        return {
            f"{self.PREFIX}-appid": self.appid,
            f"{self.PREFIX}-port": self.port,
            f"{self.PREFIX}-host": self.host,
            f"{self.PREFIX}-resource": self.resource,
            f"{self.PREFIX}-method": self.method,
            **self.authorization.to_dict(),
        }


class BaseClient:
    """
    The Client class provides a foundation for OAuth 2.0 client operations,
    including authorization, token retrieval, and authentication.
    """

    def __init__(
        self,
        provider: str,
        client_id: str,
        client_secret: str,
        grant_type: Optional[str] = None,
        response_type: Optional[str] = None,
        scope: Optional[str] = None,
        headers: Union[Dict[str, str], AuthZRequestHeaders] = {},
        redirect_uri: Optional[str] = None,
    ) -> None:
        """
        Initialize the OAuth 2.0 client with necessary credentials and parameters.

        :param client_id: The client identifier given by the OAuth provider.
        :param provider: The base URL of the OAuth provider.
        :param client_secret: The client secret used for confidential clients.
        :param kwargs: Additional parameters such as grant_type, response_type, scope, etc.
        """
        self.grant_type = grant_type
        self.response_type = response_type or "code"
        self.scope = scope or "rabc"
        self.provider = provider
        self.client_id = client_id
        self.redirect_uri = redirect_uri
        self.client_secret = client_secret
        self.headers = (
            headers.to_dict() if isinstance(headers, AuthZRequestHeaders) else headers
        )

        self._http_client = None  # Lazy initialization

    def url(self, uri: str) -> str:
        """
        Construct a full URL by joining the provider's base URL with the given URI.

        :param uri: The endpoint URI relative to the provider's base URL.
        :return: The complete URL as a string.
        """
        return urljoin(self.provider, uri)

    def default_headers(self):
        """
        Provide default HTTP headers for requests, typically setting the content type.

        :return: A dictionary containing default headers.
        """
        return {"content-type": "application/json"}

    def default_payload(self):
        return {
            "scope": self.scope,
            "client_id": self.client_id,
            "response_type": self.response_type,
            "client_secret": self.client_secret,
            "grant_type": self.grant_type,
        }

    def extend_headers(
        self, additional_headers: Union[AuthZRequestHeaders, Dict[str, str]]
    ) -> None:
        """
        Extend the default headers with additional headers provided.

        :param additional_headers: A dictionary or AuthZRequestHeaders instance with additional headers.
        :return: A dictionary containing the combined headers.
        """
        if isinstance(additional_headers, AuthZRequestHeaders):
            additional_headers = additional_headers.to_dict()
        return {**self.headers, **additional_headers}

    @property
    def client(self) -> httpx.Client:
        """
        Create an HTTP client instance with the default and custom headers.

        :return: An instance of httpx.Client with the configured headers.
        """
        headers = {**self.default_headers(), **self.headers}
        if self._http_client is None:
            self._http_client = httpx.Client(headers=headers)
        return self._http_client
