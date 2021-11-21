from solutions.CHK import checkout_solution as chk

class TestMultiPriceOffer():

    def test_applyTo(self):
        sku = 'A'
        offerContents = {sku: 1}
        offerPrice = 10
        offer = chk.MultiPriceOffer(offerContents, offerPrice)

        basket = offerContents.copy()
        assert offer.getPotentialSaving(basket) > 0
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

class TestGroupDiscountOffer():

    def test_applyTo(self):
        pass

    def test_applyToMultipleTimes(self):
        pass
