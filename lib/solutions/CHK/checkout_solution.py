#!/usr/bin/python3

ERROR_INVALID_ARGUMENT = -1

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
            return ERROR_INVALID_ARGUMENT
        totalPrice += normalPrice
    # TODO offers
    return totalPrice
