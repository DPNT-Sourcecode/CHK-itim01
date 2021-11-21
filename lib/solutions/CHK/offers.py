#!/usr/bin/python3
# -*- coding: utf-8 -*-
from solutions.CHK.includes import getTotalPrice

class MultiPriceOffer:
    """Represents a special offer in which a certain set of items can can be
       bought for a certain discounted price.
       For example: Buy 3 apples and one banana for £1"""

    def __init__(self, items, price, prices):
        """
        Parameters:
        items (dict of str: int): Mapping of what SKUs are included in
        the offer to how many of each are included.
        price (int): Discounted price itemsIncluded can be purchased for
        prices (dict of str: int): Mapping of SKU to price
        """
        self.itemsIncluded = items
        self.price = price
        self.saving = getTotalPrice(self.itemsIncluded, prices) - self.price
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

    def __init__(self, itemTypes, itemCount, price, prices):
        """
        Parameters:
        items (list of str): SKUs included in the offer.
        itemCount (int): Number of items which must be purchased.
        price (int): Discounted price itemCount items can be bought for.
        prices (dict of str: int): Mapping of SKU to price
        """
        self.itemTypes = itemTypes
        self.itemCount = itemCount
        self.price = price
        self.prices = prices

        # store itemTypes most expensive first
        self.itemTypes.sort(key=lambda sku: prices[sku], reverse=True)

    def getBestSelection(self, purchase):
        """Finds the optimum (most expensive) items from the purchase to apply
        this offer to, in order to generate the maximum possible saving.
        Returns:
        dict of str: int: Which SKUs to apply it to, and how many of each
        """
        itemsNeeded = self.itemCount
        selection = {}
        for sku in self.itemTypes:
            numInBasket = purchase.get(sku, 0)
            numToUse = min(numInBasket, itemsNeeded)
            if numToUse > 0:
                selection[sku] = numToUse
                itemsNeeded -= numToUse
            if itemsNeeded == 0:
                break
        if itemsNeeded > 0:
            return None
        return selection

    def getPotentialSaving_Internal(self, purchase):
        selection = self.getBestSelection(purchase)
        if selection is None:
            return 0, None
        saving = getTotalPrice(selection, self.prices) - self.price
        if saving < 0:
            return 0, None
        return saving, selection

    def getPotentialSaving(self, purchase):
        """See MultiPriceOffer.getPotentialSaving"""
        saving, selection = self.getPotentialSaving_Internal(purchase)
        return saving

    def applyTo(self, purchase):
        """See MultiPriceOffer.applyTo"""
        saving, selection = self.getPotentialSaving_Internal(purchase)
        if saving == 0:
            return 0
        for sku in selection:
            purchase[sku] -= selection[sku]
        return saving
