#!/usr/bin/python3

ERROR_INVALID_ARGUMENT = -1

SKU_PRICES = {
    'A': 50,
    'B': 30,
    'C': 20,
    'D': 15,
    'E': 40,
    'F': 10,
    'G': 20,
    'H': 10,
    'I': 35,
    'J': 60,
    'K': 80,
    'L': 90,
    'M': 15,
    'N': 40,
    'O': 10,
    'P': 50,
    'Q': 30,
    'R': 50,
    'S': 30,
    'T': 20,
    'U': 40,
    'V': 50,
    'W': 20,
    'X': 90,
    'Y': 10,
    'Z': 50,
}

def getTotalPrice(quantities):
    return sum(SKU_PRICES[sku] * quantities[sku] for sku in quantities)

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
        self.saving = getTotalPrice(self.itemsIncluded) - self.price
        assert self.saving > 0

    def isEligible(self, purchase):
        """Returns: bool: True if given purchase is eligible for this offer"""

        for sku in self.itemsIncluded:
            if purchase.get(sku, 0) < self.itemsIncluded[sku]:
                return False
        return True

    def applyTo(self, purchase):
        """Removes the items included in this offer from the given purchase,
        if the purchase is eligible for this offer.
        Parameters:
        purchase (dict of str: int): Mapping of SKU to quantity.
        Returns:
        bool: True if the offer was applied
        """

        if not self.isEligible(purchase):
            return False
        for sku in self.itemsIncluded:
            purchase[sku] -= self.itemsIncluded[sku]
        return True

CURRENT_OFFERS = [

    # "3A for 130"
    MultiPriceOffer({'A': 3}, 130),

    # "5A for 200"
    MultiPriceOffer({'A': 5}, 200),

    # "2B for 45"
    MultiPriceOffer({'B': 2}, 45),

    # "2E get one B free"
    MultiPriceOffer({'E': 2, 'B': 1}, getTotalPrice({'E': 2})),

    # "2F get one F free"
    MultiPriceOffer({'F': 3}, getTotalPrice({'F': 2})),

    # "5H for 45"
    MultiPriceOffer({'H': 5}, 45),

    # "10H for 80"
    MultiPriceOffer({'H': 10}, 80),

    # "2K for 150"
    MultiPriceOffer({'K': 2}, 150),

    # "3N get one M free"
    MultiPriceOffer({'N': 3, 'M': 1}, getTotalPrice({'N': 3})),

    # "5P for 200"
    MultiPriceOffer({'P': 5}, 200),

    # "3Q for 80"
    MultiPriceOffer({'Q': 3}, 80),

    # "3R get one Q free"
    MultiPriceOffer({'R': 3, 'Q': 1}, getTotalPrice({'R': 3})),

    # "3U get one U free"
    MultiPriceOffer({'U': 3}, getTotalPrice({'U': 2})),

    # "2V for 90"
    MultiPriceOffer({'V': 2}, 90),

    # "3V for 130"
    MultiPriceOffer({'V': 3}, 130)
]
CURRENT_OFFERS.sort(key=lambda o: o.saving, reverse=True)

def applyFirstOfferTo(purchase, offers):
    for offer in offers:
        if offer.applyTo(purchase):
            return offer.saving
    return 0

# noinspection PyUnusedLocal
# skus = unicode string
def checkout(skus, offers=CURRENT_OFFERS):
    """Calculates the total price of a purchase.

    Parameters:
    skus (string): The SKUs of items purchased, e.g. "AABABBACD".
    offers (list of MultiPriceOffer): Offers to apply if eligible, sorted best
    saving first.

    Returns:
    int: The total price (in the same unit as used in SKU_PRICES)
    """

    purchase = {}
    for sku in skus:
        if sku not in SKU_PRICES:
            return ERROR_INVALID_ARGUMENT
        purchase[sku] = purchase.get(sku, 0) + 1

    price = getTotalPrice(purchase)

    while True:
        saving = applyFirstOfferTo(purchase, offers)
        if saving == 0:
            break
        price -= saving

    return price

