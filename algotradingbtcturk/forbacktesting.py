from OrderManager import OrderManager
from OrderBook import OrderBook
from collections import deque
from LiquidityProvider import LiquidityProvider
from TradingStrategy import TradingStrategy
from marketforbacktesting import MarketSimulatorforbacktesting
from OrderManagerforbacktesting import OrderManagerforbacktesting
from OrderBook import OrderBook
from collections import deque

import pandas as pd
import matplotlib.pyplot as plt
import h5py

def call_if_not_empty(deg, fun):
    while (len(deg) > 0):
        fun()
class EventBasedBackTester:
    def __init__(self):
        self.lp_2_gateway = deque()
        self.ob_2_ts = deque()
        self.ts_2_om = deque()
        self.ms_2_om = deque()
        self.om_2_ts = deque()
        self.gw_2_om = deque()
        self.om_2_gw = deque()


        self.lp = LiquidityProvider(self.lp_2_gateway)
        self.ob = OrderBook(self.lp_2_gateway, self.ob_2_ts)
        self.ts = TradingStrategy(self.ob_2_ts, self.ts_2_om, self.om_2_ts)
        self.ms = MarketSimulatorforbacktesting(self.om_2_gw, self.gw_2_om)
        self.om = OrderManagerforbacktesting(self.ts_2_om, self.om_2_ts,
                               self.om_2_gw, self.gw_2_om)

    def process_data_from_yahoo(self, price):
        order_bid = {
            'id': 1,
            'price' : price,
            'quantity' : 20,
            'side' : 'bid',
            'action' : 'new'
        }
        order_ask = {
            'id': 1,
            'price': price,
            'quantity': 20,
            'side': 'ask',
            'action': 'new'
        }

        self.lp_2_gateway.append(order_ask)
        self.lp_2_gateway.append(order_bid)
        self.process_events()
        order_ask['action'] = 'delete'
        order_bid['action'] = 'delete'
        self.lp_2_gateway.append(order_ask)
        self.lp_2_gateway.append(order_bid)

    def process_events(self):
        while len(self.lp_2_gateway)>0:
            call_if_not_empty(self.lp_2_gateway, self.ob.handle_order_from_gateway)
            call_if_not_empty(self.ob_2_ts, self.ts.handle_input_from_bb)
            call_if_not_empty(self.ts_2_om, self.om.handle_input_from_ts)
            call_if_not_empty(self.om_2_gw, self.ms.handle_order_from_gw)
            call_if_not_empty(self.gw_2_om, self.om.handle_input_from_market)
            call_if_not_empty(self.om_2_ts, self.ts.handle_response_from_om)

eb = EventBasedBackTester()
import yfinance as yf

#goog_data = yf.download(tickers='BTC-USD', start='2020-06-23', end='2021-08-12')

goog_data = pd.read_csv("5.csv")
print(goog_data)
for line in zip(goog_data.index, goog_data['close']):
    date=line[0]
    price=line[1]
    price_information = {
        'date': date,
        'price' : float(price)
    }
    eb.process_data_from_yahoo(price_information['price'])
    eb.process_events()
plt.plot(eb.ts.list_pnl)
plt.plot(eb.ts.rsi_values)
plt.show()

