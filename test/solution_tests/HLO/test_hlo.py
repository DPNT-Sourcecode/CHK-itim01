from solutions.HLO import hello


class TestHlo():
    def test_sum(self):
        assert hello() == "Hello, world!"
