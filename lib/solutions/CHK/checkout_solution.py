#!/usr/bin/python3
from solutions.CHK.includes import *
from solutions.CHK import offers as offs

CURRENT_OFFERS = [

    # "3A for 130"
    offs.MultiPriceOffer({'A': 3}, 130, PRICES),

    # "5A for 200"
    offs.MultiPriceOffer({'A': 5}, 200, PRICES),

    # "2B for 45"
    offs.MultiPriceOffer({'B': 2}, 45, PRICES),

    # "2E get one B free"
    offs.MultiPriceOffer({'E': 2, 'B': 1}, getTotalPrice({'E': 2}), PRICES),

    # "2F get one F free"
    offs.MultiPriceOffer({'F': 3}, getTotalPrice({'F': 2}), PRICES),

    # "5H for 45"
    offs.MultiPriceOffer({'H': 5}, 45, PRICES),

    # "10H for 80"
    offs.MultiPriceOffer({'H': 10}, 80, PRICES),

    # "2K for 120"
    offs.MultiPriceOffer({'K': 2}, 120, PRICES),

    # "3N get one M free"
    offs.MultiPriceOffer({'N': 3, 'M': 1}, getTotalPrice({'N': 3}), PRICES),

    # "5P for 200"
    offs.MultiPriceOffer({'P': 5}, 200, PRICES),

    # "3Q for 80"
    offs.MultiPriceOffer({'Q': 3}, 80, PRICES),

    # "3R get one Q free"
    offs.MultiPriceOffer({'R': 3, 'Q': 1}, getTotalPrice({'R': 3}), PRICES),

    # "3U get one U free"
    offs.MultiPriceOffer({'U': 4}, getTotalPrice({'U': 3}), PRICES),

    # "2V for 90"
    offs.MultiPriceOffer({'V': 2}, 90, PRICES),

    # "3V for 130"
    offs.MultiPriceOffer({'V': 3}, 130, PRICES),

    # "buy any 3 of (S,T,X,Y,Z) for 45"
    offs.GroupDiscountOffer(['S', 'T', 'X', 'Y', 'Z'], 3, 45, PRICES)
]

def applyBestOffer(purchase, offers):
    if (len(offers)) == 0:
        return 0
    bestOffer = max(offers, key=lambda o: o.getPotentialSaving(purchase))
    return bestOffer.applyTo(purchase)

# noinspection PyUnusedLocal
# skus = unicode string
def checkout(skus, prices=PRICES, offers=CURRENT_OFFERS):
    """Calculates the total price of a purchase.

    Parameters:
    skus (string): The SKUs of items purchased, e.g. "AABABBACD".
    prices (dict of str to int): Mapping of SKU to price
    offers (list of offs.MultiPriceOffer): Offers to apply if eligibl, PRICESe.

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
