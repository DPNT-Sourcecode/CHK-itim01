#!/usr/bin/python3

ERROR_INVALID_ARGUMENT = -1

normalPrices = {
    'A': 50,
    'B': 30,
    'C': 20,
    'D': 15,
}

def getTotalPrice(quantities):
    return sum(normalPrices[sku] for sku in quantities)

class MultiPriceOffer:
    def __init__(self, items, price):
        self.itemsIncluded = items
        self.price = price
        self.saving = getTotalPrice(self.itemsIncluded) - self.price

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

todaysOffers = [
    MultiPriceOffer({'A': 3}, 130),
    MultiPriceOffer({'B': 2}, 45),
]
todaysOffers.sort(key=lambda o: o.saving, reverse=True)

# noinspection PyUnusedLocal
# skus = unicode string
def checkout(skus, offers=todaysOffers):
    itemQuantities = {}
    for sku in skus:
        if sku not in normalPrices:
            return ERROR_INVALID_ARGUMENT
        itemQuantities[sku] = itemQuantities.get(sku, 0) + 1

    price = getTotalPrice(itemQuantities)

    for offer in offers:
        if offer.applyTo(itemQuantities):
            price -= offer.saving

    return price




