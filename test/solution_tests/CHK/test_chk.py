from solutions.CHK import checkout_solution


class TestChk():
    
    def noItems(self):
        assert checkout_solution.checkout('') == 0

    def invalidItem(self):
        assert checkout_solution.checkout('AB9') == checkout_solution.ERROR_INVALID_ARGUMENT


