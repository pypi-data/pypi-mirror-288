import base64
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

import requests


@dataclass
class Token:
    access_token: str
    expires_at: datetime


class AuthSession:
    """This manages an OAuth session. It allows to fetch and refetch a
    JWT token from the given OAuth endpoint and stores the fetched
    token."""

    def __init__(self, client_id: str, secret: str, oauth_token_endpoint: str):
        """Initializes the AuthSession with the given client ID, secret and
        OAuth domain.

        Args:
            client_id (str): the client id.
            secret (str): the secret.
            oauth_domain (str): the OAuth2 token endpoint.
        """
        self.client_id = client_id
        self.secret = secret
        self.oauth_token_endpoint = oauth_token_endpoint

        self._current_token: Token | None = None

    def refresh_jwt_token(self) -> Token:
        """Fetches and returns a new JWT token from the OAuth2 token endpoint.

        Raises:
            Exception: the authentification failed.

        Returns:
            Token: the new JWT token and its expiration date.
        """
        bearer_token = base64.b64encode(
            f"{self.client_id}:{self.secret}".encode("utf-8")
        ).decode("utf-8")

        response = requests.post(
            self.oauth_token_endpoint,
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "Authorization": f"Basic {bearer_token}",
            },
            data={
                "grant_type": "client_credentials",
                "scope": "resource-server/api",
            },
        )

        json_response = response.json()

        if "access_token" not in json_response:
            raise Exception(
                "Authentification failed. Are your client ID and secret correct?"
            )

        access_token = str(json_response["access_token"])
        expires_in = datetime.now(tz=timezone.utc) + timedelta(
            seconds=int(json_response["expires_in"])
        )

        self._current_token = Token(access_token, expires_in)

        return self._current_token

    def get_jwt_token(self) -> str:
        """Returns the current JWT token.

        Returns:
            str: the current JWT token.
        """
        if self._current_token is None or self._current_token.expires_at < datetime.now(
            tz=timezone.utc
        ):
            self._current_token = self.refresh_jwt_token()

        return self._current_token.access_token
