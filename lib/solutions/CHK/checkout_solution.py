#!/usr/bin/python3
from offers import MultiPriceOffer

ERROR_INVALID_ARGUMENT = -1

CURRENT_PRICES = {
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

def getTotalPrice(quantities, prices=CURRENT_PRICES):
    return sum(CURRENT_PRICES[sku] * quantities[sku] for sku in quantities)

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
    MultiPriceOffer({'U': 4}, getTotalPrice({'U': 3})),

    # "2V for 90"
    MultiPriceOffer({'V': 2}, 90),

    # "3V for 130"
    MultiPriceOffer({'V': 3}, 130),
]

def applyBestOffer(purchase, offers):
    if (len(offers)) == 0:
        return 0
    bestOffer = max(offers, key=lambda o: o.getPotentialSaving(purchase))
    return bestOffer.applyTo(purchase)

# noinspection PyUnusedLocal
# skus = unicode string
def checkout(skus, prices=CURRENT_PRICES, offers=CURRENT_OFFERS):
    """Calculates the total price of a purchase.

    Parameters:
    skus (string): The SKUs of items purchased, e.g. "AABABBACD".
    prices (dict of str to int): Mapping of SKU to price
    offers (list of MultiPriceOffer): Offers to apply if eligible.

    Returns:
    int: The total price (in the same unit as used in prices)
    """

    purchase = {}
    for sku in skus:
        if sku not in prices:
            return ERROR_INVALID_ARGUMENT
        purchase[sku] = purchase.get(sku, 0) + 1

    price = getTotalPrice(purchase)

    while True:
        saving = applyBestOffer(purchase, offers)
        if saving == 0:
            break
        price -= saving

    return price

