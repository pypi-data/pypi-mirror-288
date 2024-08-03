from typing import Optional

from .types.client import Client as GraphQLClient
from .types.enums import Currency
from .types.input_types import PurchaseItemInput, PurchaseItemPriceInput
from .wraps import return_or_raise


class ConversionModule:
    def __init__(self, partner_id: str, graphql_client: GraphQLClient):
        self.partner_id = partner_id
        self.graphql_client = graphql_client

    async def estimate_given_out_fanpoints_on_purchase(
        self, purchase_items: list[PurchaseItemPriceInput]
    ):
        result = (
            await self.graphql_client.estimate_given_out_fan_points_on_purchase(
                self.partner_id,
                purchase_items,
            )
        ).estimate_given_out_fan_points_on_purchase
        return return_or_raise(result)

    async def get_price_in_fan_points(self, price: float, currency: Currency):
        result = (
            await self.graphql_client.get_price_in_fan_points(
                self.partner_id, price, currency
            )
        ).get_price_in_fan_points
        return return_or_raise(result)

    async def get_purchase(self, user_id: str, purchase_id: str):
        result = (
            await self.graphql_client.get_fan_points_transaction(
                user_id, purchase_id, self.partner_id
            )
        ).get_fan_points_transaction
        return return_or_raise(result)

    async def get_purchases(
        self,
        user_id: str,
        earlier_than: Optional[str] = None,
        limit: Optional[int] = None,
    ):
        result = (
            await self.graphql_client.get_fan_points_transactions(
                self.partner_id,
                user_id,
                limit,
                earlier_than,
            )
        ).get_fan_points_transactions
        return return_or_raise(result)

    async def give_fanpoints_on_purchase(
        self,
        user_id: str,
        purchase_items: list[PurchaseItemInput],
        custom_purchase_id: Optional[str] = None,
    ):
        result = (
            await self.graphql_client.give_fan_points_on_purchase(
                user_id, self.partner_id, purchase_items, custom_purchase_id
            )
        ).give_fan_points_on_purchase
        return return_or_raise(result)

    async def pay_purchase_with_fanpoints(
        self,
        user_id: str,
        purchase_items: list[PurchaseItemInput],
        custom_purchase_id: Optional[str] = None,
    ):
        result = (
            await self.graphql_client.pay_purchase_with_fan_points(
                user_id, self.partner_id, purchase_items, custom_purchase_id
            )
        ).pay_purchase_with_fan_points
        return return_or_raise(result)

    async def undo_transaction(
        self,
        user_id: str,
        purchase_id: str,
    ):
        result = (
            await self.graphql_client.undo_fan_points_purchase(
                user_id,
                self.partner_id,
                purchase_id,
            )
        ).undo_fan_points_purchase
        return return_or_raise(result)
