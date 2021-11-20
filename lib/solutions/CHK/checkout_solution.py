#!/usr/bin/python3

normalPrices = {
    'A': 50,
    'B': 30,
    'C': 20,
    'D': 15,
}

# noinspection PyUnusedLocal
# skus = unicode string
def checkout(skus):
    totalPrice = 0
    for sku in skus:
        normalPrice = normalPrices.get(sku)
        if (normalPrice == None):
            return -1
        totalPrice += normalPrice
    # TODO offers
    return totalPrice

