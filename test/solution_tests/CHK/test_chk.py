from solutions.CHK import checkout_solution


class TestChk():
    
    def noItems(self):
        assert checkout_solution.checkout('') == 0

    def invalidItem(self):
        assert checkout_solution.checkout('AB9') == checkout_solution.ERROR_INVALID_ARGUMENT

    def singleItem(self):
        item = 'B'
        assert checkout_solution.checkout(item) == checkout_solution.normalPrices[item]

    def oneOfEach(self):
        items = checkout_solution.normalPrices.keys()
        expected = sum([checkout_solution[sku] for sku in checkout_solution.normalPrices])
        assert checkout_solution.checkout(''.join(items)) == expected