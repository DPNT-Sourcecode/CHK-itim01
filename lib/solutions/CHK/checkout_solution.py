#!/usr/bin/python3

ERROR_INVALID_ARGUMENT = -1

SKU_PRICES = {
    'A': 50,
    'B': 30,
    'C': 20,
    'D': 15,
}

def getTotalPrice(quantities):
    return sum(SKU_PRICES[sku] * quantities[sku] for sku in quantities)

class MultiPriceOffer:
    def __init__(self, items, price):
        self.itemsIncluded = items
        self.price = price
        self.saving = getTotalPrice(self.itemsIncluded) - self.price
        assert self.saving > 0

    def isEligible(self, quantities):
        for sku in self.itemsIncluded:
            if quantities.get(sku, 0) < self.itemsIncluded[sku]:
                return False
        return True

    def applyTo(self, quantities):
        if not self.isEligible(quantities):
            return False
        for sku in self.itemsIncluded:
            quantities[sku] -= self.itemsIncluded[sku]
        return True

CURRENT_OFFERS = [
    MultiPriceOffer({'A': 3}, 130),
    MultiPriceOffer({'B': 2}, 45),
]
CURRENT_OFFERS.sort(key=lambda o: o.saving, reverse=True)

def applyFirstOfferTo(basket, offers):
    for offer in offers:
        if offer.applyTo(basket):
            return offer.saving
    return 0

# noinspection PyUnusedLocal
# skus = unicode string
def checkout(skus, offers=CURRENT_OFFERS):
    """Calculates the total price of a purchase.

    Parameters:
    skus (string): The SKUs of items purchased, e.g. "AABABBACD".
    offers (list of MultiPriceOffer): Offers to apply if eligible.

    Returns:
    int: The total price (in the same unit as used in SKU_PRICES)
    """

    basket = {}
    for sku in skus:
        if sku not in SKU_PRICES:
            return ERROR_INVALID_ARGUMENT
        basket[sku] = basket.get(sku, 0) + 1

    price = getTotalPrice(basket)

    while True:
        saving = applyFirstOfferTo(basket, offers)
        if saving == 0:
            break
        price -= saving

    return price

