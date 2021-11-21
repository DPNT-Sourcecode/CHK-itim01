#!/usr/bin/python3
# -*- coding: utf-8 -*-
import checkout_solution as chk

class MultiPriceOffer:
    """Represents a special offer in which a certain set of items can can be
       bought for a certain discounted price.
       For example: Buy 3 apples and one banana for £1"""

    def __init__(self, items, price):
        """
        Parameters:
        items (dict of str: int): Mapping of what SKUs are included in
        the offer to how many of each are included.
        price (int): Discounted price itemsIncluded can be purchased for
        """
        self.itemsIncluded = items
        self.price = price
        self.saving = chk.getTotalPrice(self.itemsIncluded) - self.price
        assert self.saving > 0

    def getPotentialSaving(self, purchase):
        """
        Returns:
        int: Money that could be saved by applying this offer,
        or 0 if the purchase is not eligible.
        """
        for sku in self.itemsIncluded:
            if purchase.get(sku, 0) < self.itemsIncluded[sku]:
                return 0
        return self.saving

    def applyTo(self, purchase):
        """Removes the items included in this offer from the given purchase,
        if the purchase is eligible for this offer.
        Parameters:
        purchase (dict of str: int): Mapping of SKU to quantity.
        Returns:
        int: Money saved by applying the offer, or 0 if not eligible
        """
        if self.getPotentialSaving(purchase) == 0:
            return 0
        for sku in self.itemsIncluded:
            purchase[sku] -= self.itemsIncluded[sku]
        return self.saving

class GroupDiscountOffer:
    """Represents a special offer in which a certain number of items from a
       given set of item types can be bough for a discounted price.
       For example: Buy any 3 fruits (A, B, C, and/or D) for £3.
       The items need not be different: The same items 3 times counts."""

    def __init__(self, itemTypes, itemCount, price, prices=chk.CURRENT_PRICES):
        """
        Parameters:
        items (list of str): SKUs included in the offer.
        itemCount (int): Number of items which must be purchased.
        price: Discounted price itemCount items can be bought for.
        """
        self.itemTypes = itemTypes
        self.itemCount = itemCount
        self.price = price

        # store itemTypes most expensive first
        self.itemTypes.sort(key=lambda sku: prices[sku], reverse=True)

    def getPotentialSaving(self, purchase):
        """See MultiPriceOffer.getPotentialSaving"""
        pass

    def applyTo(self, purchase):
        """See MultiPriceOffer.applyTo"""
        pass



