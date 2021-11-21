from solutions.CHK import offers as offers
from test.solution_tests.CHK.test_chk import TEST_PRICES

class TestMultiPriceOffer():

    def test_getPotentialSaving(self):
        sku = 'A'
        offerContents = {sku: 1}
        offerPrice = 10
        offer = offers.MultiPriceOffer(offerContents, offerPrice, TEST_PRICES)

        basket = offerContents.copy()
        assert offer.getPotentialSaving(basket) > 0
        assert offer.applyTo(basket)
        assert basket[sku] == 0
        assert offer.saving == TEST_PRICES[sku] - offerPrice

    def test_applyToMultipleTimes(self):
        offerContents = {'A': 1}
        offerPrice = 10
        offer = offers.MultiPriceOffer(offerContents, offerPrice, TEST_PRICES)

        basket = {'A': 2}
        assert offer.applyTo(basket)
        assert basket['A'] == 1
        assert offer.applyTo(basket)
        assert basket['A'] == 0
        assert not offer.applyTo(basket)

class TestGroupDiscountOffer():

    def test_getPotentialSavingNone(self):
        offer = offers.GroupDiscountOffer(['A'], 3, TEST_PRICES['A'] * 4, TEST_PRICES)
        assert offer.getPotentialSaving({'A': 3}) == 0
        pass

    def test_getPotentialSavingActual(self):
        offer = offers.GroupDiscountOffer(['A'], 1, 10, TEST_PRICES)
        assert offer.getBestSelection({'A': 1}) == {'A': 1}
        assert offer.getPotentialSaving({'A': 1}) == TEST_PRICES['A'] - 10

    def test_applyToMultipleTimes(self):
        bargain = 1
        prices = {'A': 1, 'B': 2, 'C': 3}
        offer = offers.GroupDiscountOffer(['A', 'B', 'C'], 3, bargain, prices)
        basket = {'A': 3, 'B': 3, 'C': 3}
        assert offer.applyTo(basket) == prices['C'] * 3 - bargain
        assert basket['C'] == 0
        assert basket['A'] == basket['B'] == 3
        assert offer.applyTo(basket) == prices['B'] * 3 - bargain
        assert basket['B'] == 0
        assert basket['A'] == 3
        assert offer.applyTo(basket) == prices['A'] * 3 - bargain
        assert basket['A'] == 0

