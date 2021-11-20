from unittest import TestCase
from solutions.HLO import hello_solution

class TestHlo(TestCase):
    def test_hlo(self):
        assert hello_solution.hello("World") == "Hello, World!"
        assert hello_solution.hello("Friend") == "Hello, Friend!"

    def another_test(self):
        assert False




