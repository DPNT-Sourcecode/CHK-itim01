from solutions.CHK import checkout_solution

def skuString(quantities):
    s = ""
    for sku in quantities:
        s += sku * quantities[sku]
    return s

class TestChk():

    def test_empty(self):
        assert checkout_solution.checkout('') == 0

    def test_invalidItem(self):
        assert checkout_solution.checkout('AB9') == checkout_solution.ERROR_INVALID_ARGUMENT

    def test_singleItem(self):
        item = 'B'
        assert checkout_solution.checkout(item) == checkout_solution.normalPrices[item]

    def test_oneOfEach(self):
        items = checkout_solution.normalPrices.keys()
        expected = sum([checkout_solution.normalPrices[sku] for sku in checkout_solution.normalPrices])
        assert checkout_solution.checkout(''.join(items)) == expected

    def test_singleItemOffer(self):
        sku = 'A'
        offerContents = {sku: 1}
        offerPrice = 10
        offer = checkout_solution.MultiPriceOffer(offerContents, offerPrice)

        basket = offerContents.copy()
        assert offer.isEligible(basket)
        assert offer.applyTo(basket)
        assert basket[sku] == 0
        assert offer.saving == checkout_solution.normalPrices[sku] - offerPrice

        assert checkout_solution.checkout(skuString(offerContents), offers=[offer]) == offerPrice

    def test_multiItemOffer(self):
        offerContents = {'A': 2, 'B': 2}
        offerPrice = 30
        offer = checkout_solution.MultiPriceOffer(offerContents, offerPrice)
        assert checkout_solution.checkout("AABB", offers=[offer]) == offerPrice

    def test_sameOfferMultipleTimes(self):
        offerContents = {'A': 1, 'B': 1}
        offerPrice = 30
        offer = checkout_solution.MultiPriceOffer(offerContents, offerPrice)
        skuString = "ABCAB"
        expected = offerPrice * 2 + checkout_solution.normalPrices['C']
        assert checkout_solution.checkout(skuString, offers=[offer]) == expected
