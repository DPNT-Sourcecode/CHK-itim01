from solutions.CHK import checkout_solution as chk

def skuString(quantities):
    s = ""
    for sku in quantities:
        s += sku * quantities[sku]
    return s

class TestOffer():

    def test_applyTo(self):
        sku = 'A'
        offerContents = {sku: 1}
        offerPrice = 10
        offer = chk.MultiPriceOffer(offerContents, offerPrice)

        basket = offerContents.copy()
        assert offer.isEligible(basket)
        assert offer.applyTo(basket)
        assert basket[sku] == 0
        assert offer.saving == chk.SKU_PRICES[sku] - offerPrice

    def test_applyToMultipleTimes(self):
        offerContents = {'A': 1}
        offerPrice = 10
        offer = chk.MultiPriceOffer(offerContents, offerPrice)

        basket = {'A': 2}
        assert offer.applyTo(basket)
        assert basket['A'] == 1
        assert offer.applyTo(basket)
        assert basket['A'] == 0
        assert not offer.applyTo(basket)

class TestChk():

    def test_empty(self):
        assert chk.checkout('') == 0

    def test_invalidItem(self):
        assert chk.checkout('AB9') == chk.ERROR_INVALID_ARGUMENT

    def test_singleItem(self):
        item = 'B'
        assert chk.checkout(item) == chk.SKU_PRICES[item]

    def test_oneOfEach(self):
        items = chk.SKU_PRICES.keys()
        expected = sum([chk.SKU_PRICES[sku] for sku in chk.SKU_PRICES])
        assert chk.checkout(''.join(items)) == expected

    def test_singleItemOffer(self):
        offerContents = {'A': 1}
        offerPrice = 10
        offer = chk.MultiPriceOffer(offerContents, offerPrice)
        assert chk.checkout('A', [offer]) == offerPrice

    def test_multiItemOffer(self):
        offerContents = {'A': 2, 'B': 2}
        offerPrice = 30
        offer = chk.MultiPriceOffer(offerContents, offerPrice)
        assert chk.checkout("AABB", [offer]) == offerPrice

    def test_sameOfferMultipleTimes(self):
        offerContents = {'A': 1}
        offerPrice = 10
        offer = chk.MultiPriceOffer(offerContents, offerPrice)
        assert chk.checkout("A", [offer]) == 10
        assert chk.checkout("AA", [offer]) == 20
        assert chk.checkout("AAA", [offer]) == 30
        assert chk.checkout("AAAB", [offer]) == 30 + chk.SKU_PRICES['B']
        assert chk.checkout("ABAA", [offer]) == 30 + chk.SKU_PRICES['B']

    def test_multiItemOfferMultipleTimes(self):
        offerContents = {'A': 1, 'B': 1}
        offerPrice = 30
        offer = chk.MultiPriceOffer(offerContents, offerPrice)
        skuString = "ABCAB"
        expected = offerPrice * 2 + chk.SKU_PRICES['C']
        assert chk.checkout(skuString, [offer]) == expected

    def test_multipleOffers(self):
        of1 = chk.MultiPriceOffer({'A': 1}, 10)
        of2 = chk.MultiPriceOffer({'B': 1}, 10)
        assert chk.checkout("AB", [of1]) == 10 + chk.SKU_PRICES['B']
        assert chk.checkout("AB", [of2]) == chk.SKU_PRICES['A'] + 10
        assert chk.checkout("AB", [of1, of2]) == 20

    def test_multipleCompetingOffers(self):
        of1 = chk.MultiPriceOffer({'A': 1}, 20)
        of2 = chk.MultiPriceOffer({'A': 4}, 60)
        assert chk.checkout("AAAA", [of1, of2]) == 80
        assert chk.checkout("AAAA", [of2, of1]) == 60 # sorted by best saving

    def test_two_e_one_b_free(self):
        assert chk.checkout("EEB") == chk.SKU_PRICES["E"] * 2
        assert chk.checkout("BEE") == chk.SKU_PRICES["E"] * 2

    def test_two_f_get_one_f_free(self):
        assert chk.checkout("FF") == chk.SKU_PRICES["F"] * 2
        assert chk.checkout("FFF") == chk.SKU_PRICES["F"] * 2
        assert chk.checkout("FFF", []) == chk.SKU_PRICES["F"] * 3
        assert chk.checkout("FFFF") == chk.SKU_PRICES["F"] * 3
        assert chk.checkout("FFFFF") == chk.SKU_PRICES["F"] * 4
        assert chk.checkout("FFFFFF") == chk.SKU_PRICES["F"] * 4
        assert chk.checkout("FFFFFFF") == chk.SKU_PRICES["F"] * 5


