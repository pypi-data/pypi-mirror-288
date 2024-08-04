from datetime import datetime
from typing import Optional

from fanpoints_python.date_utils import is_naive

from .return_or_raise import ResponseError, return_or_raise
from .types.client import Client as GraphQLClient
from .types.enums import Currency
from .types.input_types import PurchaseItemInput, PurchaseItemPriceInput


class ConversionModule:
    """The conversion module contains methods revolving around purchases by Fanpoints users at Marketing
    Partners. It allows you to give users FanPoints on purchases and to let users pay with FanPoints.
    Furthermore, some convenience methods such as retrieving registered purchases or converting
    FanPoints to CHF are provided."""

    def __init__(self, partner_id: str, graphql_client: GraphQLClient):
        self.partner_id = partner_id
        self.graphql_client = graphql_client

    async def estimate_given_out_fanpoints_on_purchase(
        self, purchase_items: list[PurchaseItemPriceInput]
    ) -> int:
        """Estimates the amount of FanPoints that will be given out for a purchase.

        This allows you to check how many FanPoints will the user receive without
        actually making a purchase. Use the method `pay_purchase_with_fanpoints`
        to actually make a purchase.

        Args:
            purchase_items (list[PurchaseItemPriceInput]):
                The items that will be purchased. Each item must have a price and
                a currency. Optionally, you can also provide a commission rate label
                ("Provisions-Modell").

        Returns:
            int: The amount of FanPoints that would be given out for the purchase.

        Raises:
            ResponseError: with error code `invalid_rate_label_error` if the rate label
                is not known.
        """
        result = (
            await self.graphql_client.estimate_given_out_fan_points_on_purchase(
                self.partner_id,
                purchase_items,
            )
        ).estimate_given_out_fan_points_on_purchase
        return return_or_raise(result)

    async def get_price_in_fan_points(self, price: float, currency: Currency):
        """Returns the FanPoints price for a given price in CHF.

        Args:
            price (float): the price in CHF.
            currency (Currency): the currency of the price.

        Returns:
            the FanPoints price for the given price in CHF.

        Raises:
            ResponseError:
                if the given price is not valid (`invalid_reward_amount_error`).
        """
        result = (
            await self.graphql_client.get_price_in_fan_points(
                self.partner_id, price, currency
            )
        ).get_price_in_fan_points
        return return_or_raise(result)

    async def get_purchase(self, user_id: str, purchase_id: str):
        """Returns the details of a purchase.

        Args:
            user_id (str): the id of the user that made the purchase.
            purchase_id (str): the id of the purchase.

        Returns:
            the purchase details.

        Raises:
            ResponseError:
                if the user does not exist (`unknown_user_error`),
                if the given purchase id is not valid (`transaction_not_found_error`).
        """
        result = (
            await self.graphql_client.get_fan_points_transaction(
                user_id, purchase_id, self.partner_id
            )
        ).get_fan_points_transaction
        return return_or_raise(result)

    async def get_purchases(
        self,
        user_id: Optional[str] = None,
        earlier_than: Optional[datetime] = None,
        limit: Optional[int] = None,
    ):
        """Returns all registered purchases at the Marketing Partner.

        The returned transactions contains both transactions where the user
        received FanPoints on a purchase and transactions where the user purchased
        using FanPoints. Undo-transactions are also included.

        If `userId` is given, only transactions for this user will be returned.

        If `limit` is given, at most `limit` transactions
        will be returned. If `earlier_than` is given, only transactions
        that happened before this date will be returned. Combine
        both parameters to paginate the results.

        Args:
            user_id (Optional[str], optional):
                the id of the user to filter for. Defaults to None.
            earlier_than (Optional[datetime], optional):
                if given, transactions before this date will be returned. Defaults to None.
            limit (Optional[int], optional):
                the maximum number of transactions to return. Defaults to None.

        Returns:
            a list of the transactions.

        Raises:
            ResponseError:
                if the user does not exist (`unknown_user_error`),
                if the given date is not aware (`naive_earlier_than`).
        """
        if earlier_than and is_naive(earlier_than):
            raise ResponseError(
                "earlier_than must be a timezone aware datetime", ["naive_earlier_than"]
            )

        result = (
            await self.graphql_client.get_fan_points_transactions(
                self.partner_id,
                user_id,
                limit,
                str(earlier_than) if earlier_than else None,
            )
        ).get_fan_points_transactions
        return return_or_raise(result)

    async def give_fanpoints_on_purchase(
        self,
        user_id: str,
        purchase_items: list[PurchaseItemInput],
        custom_purchase_id: Optional[str] = None,
    ):
        """Gives FanPoints to the user for the given purchase and purchase items.

        The titles and descriptions can be used to add human readable information on the
        transaction that could be used to display to the user.

        Each purchase item can have a different rate label in order to specify the conversion rate
        from the price to the number of FanPoints. If no rate label is given, the
        default rate of the Marketing Partner will be used.

        A custom purchase id can be given in order to link the transaction to a specific event
        on your side. This operation is idempotent w.r.t. the purchase group id. This means that
        if you call this method twice with the same custom purchase id, the second call will not have
        any effect and an error will be raised.

        Args:
            user_id (str): the id of the user to give FanPoints to.
            purchase_items (list[PurchaseItemInput]): the items that were purchased.
            custom_purchase_id (Optional[str], optional): an optional custom purchase id. Defaults to None.

        Returns:
            a list of the resulting purchase transactions.

        Raises:
            ResponseError:
                if the user does not exist (`unknown_user_error`),
                if the given price is not valid (`invalid_reward_amount_error`), if the custom
                purchase id is not valid (`invalid_transaction_id_error`), if a transaction
                with the given custom purchase id already exists (`already_executed_error`),
                if the given custom purchase item ids are not unique (`non_unique_purchase_item_ids_error`),
                or if one of the rate labels does not exist (`invalid_rate_label_error`).
        """
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
        """Allows a user to pay a purchase using FanPoints.

        The titles and descriptions can be used to add human readable information on the
        transaction that could be used to display to the user.

        A custom purchase id can be given in order to link the transaction to a specific event
        on your side. This operation is idempotent w.r.t. the purchase purchase id. This means that
        if you call this method twice with the same custom purchase id, the second call will not have
        any effect and an error will be raised.

        Args:
            user_id (str):
                the id of the user to pay the purchase with FanPoints.
            purchase_items (list[PurchaseItemInput]):
                the items that were purchased.
            custom_purchase_id (Optional[str], optional):
                an optional custom purchase id. Defaults to None.

        Returns:
            a list of the resulting purchase transactions.

        Raises:
            ResponseError:
                if the user does not exist (`unknown_user_error`),
                if the given price is not valid (`invalid_reward_amount_error`), if the custom
                purchase id is not valid (`invalid_transaction_id_error`), if a transaction
                with the given custom purchase id already exists (`already_executed_error`),
                if the given custom purchase item ids are not unique (`non_unique_purchase_item_ids_error`),
                or if the user does not have enough FanPoints (`too_few_available_error`).
        """
        result = (
            await self.graphql_client.pay_purchase_with_fan_points(
                user_id, self.partner_id, purchase_items, custom_purchase_id
            )
        ).pay_purchase_with_fan_points
        return return_or_raise(result)

    async def undo_purchase_item(
        self, user_id: str, purchase_id: str, purchase_item_id: str
    ):
        """Cancels a purchase item.

        This will reverse the effect of giving out FanPoints or paying with FanPoints.

        Note that undoing a purchase might not be possible, e.g. if the FanPoints have already been
        spent by the user.

        Undoing a purchase corresponds to creating a new purchase with a negative price.
        This operation is idempotent w.r.t. the purchase id and purchase item id. This means
        that if you call this method twice with the same arguments, the second call will not
        have any effect and an error will be raised.

        Args:
            user_id (str): the id of the user that made the purchase.
            purchase_id (str): the id of the purchase.
            purchase_item_id (str): the id of the purchase item.

        Returns:
            the undo purchase details.

        Raises:
            ResponseError:
                if the user does not exist (`unknown_user_error`),
                if the given purchase id is not valid (`transaction_not_found_error`),
                if the given purchase item id is not valid (`transaction_not_found_error`),
                if the given purchase item id is not part of the given purchase (`transaction_not_found_error`),
                if the a distribution cannot be undone as the user has already spent the FanPoints (`too_few_available_error`),
                if the purchase item has already been undone (`already_executed_error`).
        """
        result = (
            await self.graphql_client.undo_fan_points_purchase(
                user_id, self.partner_id, purchase_id, purchase_item_id
            )
        ).undo_fan_points_purchase
        return return_or_raise(result)
