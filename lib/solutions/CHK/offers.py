import checkout_solution as chk

class MultiPriceOffer:
    """Represents a special offer in which a certain set of items can can be
       bought for a certain discounted price"""

    def __init__(self, items, price):
        """
        Parameters:
        itemsIncluded (dict of str: int): Mapping of what SKUs are included in
        the offer to how many of each are included.
        price (int): Discounted price itemsIncluded can be purchased for, in the
        same units as SKU_PRICES
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
