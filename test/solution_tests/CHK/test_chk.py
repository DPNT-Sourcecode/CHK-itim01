from solutions.CHK import checkout_solution as chk

TEST_PRICES = {
    'A': 50,
    'B': 30,
    'C': 20,
    'D': 15,
    'E': 40,
    'F': 10,
}

class TestChk():

    def test_empty(self):
        assert chk.checkout('') == 0

    def test_invalidItem(self):
        assert chk.checkout('AB9') == chk.ERROR_INVALID_ARGUMENT

    def test_singleItem(self):
        item = 'B'
        assert chk.checkout(item) == TEST_PRICES[item]

    def test_oneOfEach(self):
        items = TEST_PRICES.keys()
        expected = sum([TEST_PRICES[sku] for sku in TEST_PRICES])
        assert chk.checkout(''.join(items)) == expected

    def test_singleItemOffer(self):
        offerContents = {'A': 1}
        offerPrice = 10
        offer = chk.MultiPriceOffer(offerContents, offerPrice)
        assert chk.checkout('A', TEST_PRICES, [offer]) == offerPrice

    def test_multiItemOffer(self):
        offerContents = {'A': 2, 'B': 2}
        offerPrice = 30
        offer = chk.MultiPriceOffer(offerContents, offerPrice)
        assert chk.checkout('AABB', TEST_PRICES, [offer]) == offerPrice

    def test_sameOfferMultipleTimes(self):
        offerContents = {'A': 1}
        offerPrice = 10
        offer = chk.MultiPriceOffer(offerContents, offerPrice)
        assert chk.checkout('A', TEST_PRICES, [offer]) == 10
        assert chk.checkout('AA', TEST_PRICES, [offer]) == 20
        assert chk.checkout('AAA', TEST_PRICES, [offer]) == 30
        assert chk.checkout('AAAB', TEST_PRICES, [offer]) == 30 + TEST_PRICES['B']
        assert chk.checkout('ABAA', TEST_PRICES, [offer]) == 30 + TEST_PRICES['B']

    def test_multiItemOfferMultipleTimes(self):
        offerContents = {'A': 1, 'B': 1}
        offerPrice = 30
        offer = chk.MultiPriceOffer(offerContents, offerPrice)
        skuString = 'ABCAB'
        expected = offerPrice * 2 + TEST_PRICES['C']
        assert chk.checkout(skuString, TEST_PRICES, [offer]) == expected

    def test_multipleOffers(self):
        of1 = chk.MultiPriceOffer({'A': 1}, 10)
        of2 = chk.MultiPriceOffer({'B': 1}, 10)
        assert chk.checkout('AB', TEST_PRICES, [of1]) == 10 + TEST_PRICES['B']
        assert chk.checkout('AB', TEST_PRICES, [of2]) == TEST_PRICES['A'] + 10
        assert chk.checkout('AB', TEST_PRICES, [of1, of2]) == 20

    def test_multipleCompetingOffers(self):
        of1 = chk.MultiPriceOffer({'A': 1}, 20)
        of2 = chk.MultiPriceOffer({'A': 4}, 60)
        assert chk.checkout('AAAA', TEST_PRICES, [of1, of2]) == 60
        assert chk.checkout('AAAA', TEST_PRICES, [of2, of1]) == 60

    def test_two_e_one_b_free(self):
        offer = chk.MultiPriceOffer({'E': 2, 'B': 1}, chk.getTotalPrice({'E': 2}))
        assert chk.checkout('EEB', TEST_PRICES, [offer]) == TEST_PRICES['E'] * 2
        assert chk.checkout('BEE', TEST_PRICES, [offer]) == TEST_PRICES['E'] * 2

    def test_two_f_get_one_f_free(self):
        offer = chk.MultiPriceOffer({'F': 3}, chk.getTotalPrice({'F': 2}))
        assert chk.checkout('FF', TEST_PRICES, [offer]) == TEST_PRICES['F'] * 2
        assert chk.checkout('FFF', TEST_PRICES, [offer]) == TEST_PRICES['F'] * 2
        assert chk.checkout('FFF', TEST_PRICES, []) == TEST_PRICES['F'] * 3
        assert chk.checkout('FFFF', TEST_PRICES, [offer]) == TEST_PRICES['F'] * 3
        assert chk.checkout('FFFFF', TEST_PRICES, [offer]) == TEST_PRICES['F'] * 4
        assert chk.checkout('FFFFFF', TEST_PRICES, [offer]) == TEST_PRICES['F'] * 4
        assert chk.checkout('FFFFFFF', TEST_PRICES, [offer]) == TEST_PRICES['F'] * 5

    def test_singleItemGroupDiscountOffer(self):
        offer = chk.GroupDiscountOffer(['A'], 1, 10, TEST_PRICES)
        assert chk.checkout('A', TEST_PRICES, [offer]) == 10
        assert chk.checkout('B', TEST_PRICES, [offer]) == TEST_PRICES['B']
        offer = chk.GroupDiscountOffer(['A', 'B'], 1, 10, TEST_PRICES)
        assert chk.checkout('A', TEST_PRICES, [offer]) == 10
        assert chk.checkout('B', TEST_PRICES, [offer]) == 10
        assert chk.checkout('AB', TEST_PRICES, [offer]) == 10 + (TEST_PRICES[c] for c in 'AB')
        offer = chk.GroupDiscountOffer(['B', 'A'], 1, 10, TEST_PRICES)
        assert chk.checkout('A', TEST_PRICES, [offer]) == 10
        assert chk.checkout('B', TEST_PRICES, [offer]) == 10
        assert chk.checkout('AB', TEST_PRICES, [offer]) == 10 + min(TEST_PRICES[c] for c in 'AB')

    def test_multiItemGroupDiscountOffer(self):
        offer = chk.GroupDiscountOffer(['A', 'B', 'C'], 2, 20, TEST_PRICES)
        assert chk.checkout('AA', TEST_PRICES, [offer]) == 20
        assert chk.checkout('BB', TEST_PRICES, [offer]) == 20
        assert chk.checkout('CC', TEST_PRICES, [offer]) == 20
        assert chk.checkout('AB', TEST_PRICES, [offer]) == 20
        assert chk.checkout('BC', TEST_PRICES, [offer]) == 20
        assert chk.checkout('CA', TEST_PRICES, [offer]) == 20

    def test_groupDiscountOfferMultipleTimes(self):
        offer = chk.GroupDiscountOffer(['A', 'B'], 2, 10, TEST_PRICES)
        assert chk.checkout('AAAAAA', TEST_PRICES, [offer]) == 10 * 3
        assert chk.checkout('AAABBB', TEST_PRICES, [offer]) == 10 * 3

    def test_multipleGroupDiscountOffers(self):
        of1 = chk.GroupDiscountOffer(['A', 'B'], 2, 10, TEST_PRICES)
        of2 = chk.GroupDiscountOffer(['C', 'D'], 2, 10, TEST_PRICES)
        assert chk.checkout('ABCD', TEST_PRICES, [of1, of2]) == 20

    def test_multipleCompetingGroupDiscountOffers(self):
        of1 = chk.GroupDiscountOffer(['C'], 2, 20, TEST_PRICES)
        of2 = chk.GroupDiscountOffer(['A', 'B', 'C'], 3, 30, TEST_PRICES)
        assert chk.checkout('ABCC', TEST_PRICES, [of1, of2]) == 20 + TEST_PRICES['C']

    def test_groupDiscountAndMultiBuy(self):
        of1 = chk.GroupDiscountOffer(['A', 'B', 'C'], 3, 20, TEST_PRICES)
        of2 = chk.MultiPriceOffer({'A': 1, 'B': 1, 'C': 1}, 30)
        assert chk.checkout('ABC', TEST_PRICES, [of1, of2]) == 20
        of1 = chk.GroupDiscountOffer(['A', 'B', 'C'], 3, 40, TEST_PRICES)
        of2 = chk.MultiPriceOffer({'A': 1, 'B': 1, 'C': 1}, 30)
        assert chk.checkout('ABC', TEST_PRICES, [of1, of2]) == 30
        assert chk.checkout('ABCCCC', TEST_PRICES, [of1, of2]) == 30 + 40

