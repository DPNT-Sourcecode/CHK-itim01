#!/usr/bin/python3

ERROR_INVALID_ARGUMENT = -1

normalPrices = {
    'A': 50,
    'B': 30,
    'C': 20,
    'D': 15,
}

def getTotalPrice(quantities):
    return sum(quantities[sku] for sku in quantities)

class MultiPriceOffer:
    def __init__(self, items, price):
        self.itemsIncluded = items
        self.price = price

    def getSaving(self):
        return self.price - getTotalPrice(self.itemsIncluded)

    def isEligible(self, quantities):
        for sku in self.itemsIncluded:
            if quantities[sku] < self.itemsIncluded.get(sku, 0):
                return False
        return True

todaysOffers = [
    MultiPriceOffer({'A': 3}, 130),
    MultiPriceOffer({'B': 2}, 45),
]
todaysOffers.sort(key=lambda o: o.getSaving(), reverse=True)

# noinspection PyUnusedLocal
# skus = unicode string
def checkout(skus):
    itemQuantities = {}
    for sku in skus:
        if sku not in normalPrices:
            return ERROR_INVALID_ARGUMENT
        itemQuantities[sku] = itemQuantities.get(sku, 0) + 1

    price = getTotalPrice(itemQuantities)

    while True:
        for offer in todaysOffers:
            if offer.isEligible(itemQuantities):



