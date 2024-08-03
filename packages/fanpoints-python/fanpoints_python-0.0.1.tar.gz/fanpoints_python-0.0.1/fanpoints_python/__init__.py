from .backendConfig import GRAPHQL_ENDPOINT, OAUTH_TOKEN_ENDPOINT
from .fanpoints_client import FanpointsClient


def create_client(partner_id: str, client_id: str, secret: str) -> FanpointsClient:
    """Instantiates a FanpointsClient that can be used to interact with the Fanpoints API
    as a Marketing Partner.

    Args:
        partner_id (str): the ID of your Marketing Partner.
        client_id (str): the client ID. You can generate this in the Fanpoints dashboard.
        secret (str): the client secret. You can generate this in the Fanpoints dashboard.

    Returns:
        FanpointsClient:
            the FanpointsClient instance that you can use to interact
            with the Fanpoints API.
    """
    return FanpointsClient(
        partner_id, client_id, secret, OAUTH_TOKEN_ENDPOINT, GRAPHQL_ENDPOINT
    )
