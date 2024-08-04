from .types.client import Client as GraphQLClient


class UserModule:
    """This class provides methods to work with Fanpoint user ids."""

    def __init__(self, partner_id: str, graphql_client: GraphQLClient):
        self.partner_id = partner_id
        self.graphql_client = graphql_client

    def is_valid_user_id(self, user_id: str) -> bool:
        """Checks if the given user_id is valid.

        The user_id should be a 12-digit number. The last digit is a checksum digit.
        The checksum digit uses the same algorithm as the UPC-A checksum."""
        if len(user_id) != 12 or not user_id.isdigit():
            return False

        digits = [int(d) for d in user_id]

        odd_sum = sum(digits[0::2])
        even_sum = sum(digits[1::2])
        checksum = 3 * odd_sum + even_sum

        return checksum % 10 == 0

    def format_user_id(self, user_id: str) -> str:
        """Adds spaces to the user_id such that the numbers are
        grouped in groups of 4 digits."""
        return " ".join(user_id[i : i + 4] for i in range(0, len(user_id), 4))

    async def does_user_exist(self, user_id: str) -> bool:
        """Checks if the given user_id exists."""
        if not self.is_valid_user_id(user_id):
            return False

        return (
            await self.graphql_client.does_user_exist(self.partner_id, user_id)
        ).does_user_exist.result
