import unittest
from LiquidityProvider import LiquidityProvider

class TestMarketSimulator(unittest.TestCase):
    def setUp(self):
        self.liquidity_provider = LiquidityProvider()

    def test_add_liquidity(self):
        self.liquidity_provider.gettingprices()

        self.assertEqual(len(self.liquidity_provider.orders), 2)
        self.assertEqual(self.liquidity_provider.orders[0]['id'], 1)
        self.assertEqual(self.liquidity_provider.orders[1]['side'], 'buy')


