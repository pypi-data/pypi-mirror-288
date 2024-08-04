from httpx import AsyncClient as AsyncHttpxClient
from httpx import Request

from .auth_session import AuthSession
from .backendConfig import GRAPHQL_ENDPOINT, OAUTH_TOKEN_ENDPOINT
from .conversion_module import ConversionModule
from .types.client import Client as GraphQLClient
from .types.ping import Ping
from .user_module import UserModule


class FanpointsClient:
    """This class provides access to the Fanpoints API as a Marketing Partner.

    Use the submodules `conversion` and `users` to interact with the Fanpoints API.
    You can check if the client is correctly configured by calling the `ping` method.
    """

    def _sign_request(self, request: Request) -> Request:
        request.headers["Authorization"] = self.auth_session.get_jwt_token()
        return request

    def _get_graphql_client(self, graphql_endpoint: str) -> GraphQLClient:
        httpx_client = AsyncHttpxClient(auth=self._sign_request)
        return GraphQLClient(url=graphql_endpoint, http_client=httpx_client)

    def __init__(
        self,
        partner_id: str,
        client_id: str,
        secret: str,
    ):
        self.partner_id = partner_id
        self.auth_session = AuthSession(client_id, secret, OAUTH_TOKEN_ENDPOINT)
        self.graphql_client = self._get_graphql_client(GRAPHQL_ENDPOINT)

        self.conversion = ConversionModule(self.partner_id, self.graphql_client)
        self.users = UserModule(self.partner_id, self.graphql_client)

    async def ping(self) -> Ping:
        """Checks if the client is correctly configured by calling the Fanpoints API.
        If everything is configured correctly, the method returns a Ping object.
        Otherwise, it raises an exception.

        Returns:
            Ping: the response from the Fanpoints API.

        Raises:
            Exception: if the client is not configured correctly.
        """
        return await self.graphql_client.ping()
