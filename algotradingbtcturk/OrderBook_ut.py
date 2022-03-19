import unittest
from OrderBook import OrderBook


class TestOrderBook(unittest.TestCase):
    def setUp(self):
        self.reforderbook = OrderBook()

    def test_handlenew(self):


        order1 = {
            'id' : 1,
            'price': 219,
            'quantity':10,
            'side':'sell',
            'action': 'new'
        }
        ob_for_appl =self.reforderbook
        ob_for_appl.handle_new(order1)
        self.assertEqual(ob_for_appl.list_bids[0]['id'], 1)

