from datetime import datetime
import logging
from enum import Enum
from typing import Dict, Union, Optional
from pydantic import BaseModel, ConfigDict

from authz import BaseClient, AuthZRequestHeaders, Token


class User(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    open_id: str
    username: str
    email: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    is_active: bool
    email_verified: bool
    last_activity: Optional[datetime]
    nickname: Optional[str]
    avatar_url: Optional[str]
    gender: Optional[str]
    birthdate: Optional[datetime]


class AuthType(str, Enum):
    PASSWORD = "password"
    EMAIL_CODE = "email_code"
    PHONE_CODE = "phone_code"

    def to_snake_case(self):
        return self.name.lower().replace("_", "")


class UserCredentials(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    auth_type: AuthType
    auth_value: str
    auth_account: str


class AuthClient(BaseClient):
    """
    The Account class extends the Client class to provide account-specific functionality.
    """

    def login(self, payload: Union[Dict[str, str], UserCredentials]) -> Token:
        """
        Log in a user with the given credentials and return a Token object.

        :param payload: A dictionary or UserCredentials object containing the login credentials.
        :return: A Token object representing the authentication token.
        """
        url = self.url("/auth/login")
        response = self.client.post(url, json=payload.model_dump())
        logging.debug(response.json())
        response.raise_for_status()
        return Token(**response.json())

    def logout(self, headers_ext: Union[Dict[str, str], AuthZRequestHeaders]) -> bool:
        """
        Log out the current user by sending a POST request to the logout endpoint.

        :param headers_ext: Extended headers to include in the logout request.
        :return: True if the logout was successful, False otherwise.
        """
        url = self.url("/auth/logout")
        response = self.client.post(url, headers=self.extend_headers(headers_ext))
        logging.debug(response.json())
        response.raise_for_status()
        return True


class AccountClient(BaseClient):

    def me(self, headers_ext: Union[Dict[str, str], AuthZRequestHeaders]) -> User:
        url = self.url("/users/me")
        response = self.client.post(url, headers=self.extend_headers(headers_ext))
        logging.debug(response.json())
        response.raise_for_status()
        return User(**response.json())

    def profile(
        self,
        identifier: str,
        headers_ext: Union[Dict[str, str], AuthZRequestHeaders],
    ) -> User:
        url = self.url("/users/info")
        response = self.client.post(
            url,
            json={"username": identifier, "open_id": identifier, "email": identifier},
            headers=self.extend_headers(headers_ext),
        )
        print(response.json())
        logging.debug(response.json())
        response.raise_for_status()
        return User(**response.json())
