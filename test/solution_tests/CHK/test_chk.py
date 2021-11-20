from solutions.CHK import checkout_solution

def skuString(quantities):
    s = ""
    for sku in quantities:
        s += sku * quantities[sku]

class TestChk():

    def test_chk(self):
        assert checkout_solution.checkout('') == 0

    # TODO: Figure out how to have more than one unit test in python

    def invalidItem(self):
        assert checkout_solution.checkout('AB9') == checkout_solution.ERROR_INVALID_ARGUMENT

    def singleItem(self):
        item = 'B'
        assert checkout_solution.checkout(item) == checkout_solution.normalPrices[item]

    def oneOfEach(self):
        items = checkout_solution.normalPrices.keys()
        expected = sum([checkout_solution[sku] for sku in checkout_solution.normalPrices])
        assert checkout_solution.checkout(''.join(items)) == expected

    def oneOffer(self):
        offerContents = {'A': 1}
        offerPrice = 10
        offer = checkout_solution.MultiPriceOffer(offerContents, offerPrice)
        assert checkout_solution.checkout(skuString(offerContents), offerPrice)
