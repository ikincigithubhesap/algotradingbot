from time import sleep
from market import MarketSimulator
from OrderManager import OrderManager
from LiquidityProvider import LiquidityProvider
from TradingStrategy import TradingStrategy
from OrderBook import OrderBook
from marketforbacktesting import MarketSimulatorforbacktesting
from OrderManagerforbacktesting import OrderManagerforbacktesting
from collections import deque

class EventBasedBackTester:
    def __init__(self):
        self.livedatatimer = 0
        self.orders = []
        self.order_id = 0
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
        self.ms = MarketSimulator(self.om_2_gw, self.gw_2_om)
        self.om = OrderManager(self.ts_2_om, self.om_2_ts,
                               self.om_2_gw, self.gw_2_om)

    def load_historical_data(self, price):
        self.order_id += 1
        ord_sell = {
            'id': self.order_id,
            'price': price,
            'quantity': 20,
            'side': 'bid',
            'action': 'new'
        }
        ord_buy = {
            'id': self.order_id,
            'price': price,
            'quantity': 20,
            'side': 'ask',
            'action': 'new'
        }

        self.lp_2_gateway.append(ord_sell)
        self.lp_2_gateway.append(ord_buy)
    def process_data(self, price=None):
        import time, base64, hmac, hashlib, requests, json
        print(self.lp_2_gateway)
        """"
        self.order_id += 1
        ord_sell = {
            'id': self.order_id,
            'price': price,
            'quantity': 1000,
            'side': 'bid',
            'action': 'new'
        }
        ord_buy = {
            'id': self.order_id,
            'price': price,
            'quantity': 1000,
            'side': 'ask',
            'action': 'new'
        }

        self.lp_2_gateway.append(ord_sell)
        self.process_events()
        self.lp_2_gateway.append(ord_buy)
        self.process_events()
        ord_sell['action'] = 'delete'
        ord_buy['action'] = 'delete'
        self.lp_2_gateway.append(ord_buy)
        self.process_events()
        self.lp_2_gateway.append(ord_sell)
        self.livedatatimer +=1
    
        import pandas as pd
        goog_data = pd.read_csv("5.csv")
        for line in zip(goog_data.index, goog_data['close']):
            date = line[0]
            price = line[1]
            price_information = {
                'date': date,
                'price': float(price)
            }
            eb.ts.create_metrics_with_prices(price_information["price"])
         
    
        if True:
            base = "https://api.btcturk.com"
            method = "/api/v2/orderbook?pairSymbol=BTC_USDT"
            uri = base + method
            import pandas as pd
            result = requests.get(url=uri)
            result = result.json()
            # result = pd.DataFrame.from_dict(result)

            if result['success']:
                self.bestbidprice = result['data']['bids'][0][0]
                self.bestbidamount = result['data']['bids'][0][1]
                self.bestaskprice = result['data']['asks'][0][0]
                self.bestaskamount = result['data']['asks'][0][1]

            self.order_id += 1
            ord_sell = {
                'id': self.order_id,
                'price': float(self.bestbidprice),
                'quantity': 10,
                'side': 'bid',
                'action': 'new'
            }
            ord_buy = {
                'id': self.order_id,
                'price': float(self.bestaskprice),
                'quantity': 10,
                'side': 'ask',
                'action': 'new'
            }

            self.lp_2_gateway.append(ord_sell)
            print(self.lp_2_gateway)
            self.process_events()
            self.lp_2_gateway.append(ord_buy)
            self.process_events()
            ord_sell['action'] = 'delete'
            ord_buy['action'] = 'delete'
            self.lp_2_gateway.append(ord_buy)
            self.process_events()
            self.lp_2_gateway.append(ord_sell)
            self.process_events()
            """

        while True:

                sleep(900)
                base = "https://api.btcturk.com"
                method = "/api/v2/orderbook?pairSymbol=BTC_USDT"
                uri = base + method
                import pandas as pd
                result = requests.get(url=uri)
                result = result.json()
            # result = pd.DataFrame.from_dict(result)

                if result['success']:
                    self.bestbidprice = result['data']['bids'][0][0]
                    self.bestbidamount = result['data']['bids'][0][1]
                    self.bestaskprice = result['data']['asks'][0][0]
                    self.bestaskamount = result['data']['asks'][0][1]

                self.order_id += 1
                ord_sell = {
                    'id': self.order_id,
                    'price': float(self.bestbidprice),
                    'quantity': 20,
                    'side': 'bid',
                    'action': 'new'
                }
                ord_buy = {
                    'id': self.order_id,
                    'price': float(self.bestaskprice),
                    'quantity': 20,
                    'side': 'ask',
                    'action': 'new'
                }

                self.lp_2_gateway.append(ord_sell)
                print(self.lp_2_gateway)
                self.process_events()
                self.lp_2_gateway.append(ord_buy)
                self.process_events()
                ord_sell['action'] = 'delete'
                ord_buy['action'] = 'delete'
                self.lp_2_gateway.append(ord_buy)
                self.process_events()
                self.lp_2_gateway.append(ord_sell)
                self.process_events()






    def call_if_not_empty(self, deg, fun):
        while (len(deg) > 0):
            fun()

    def process_events(self):
        while len(self.lp_2_gateway)>0:
            self.call_if_not_empty(self.lp_2_gateway, self.ob.handle_order_from_gateway)
            self.call_if_not_empty(self.ob_2_ts, self.ts.handle_input_from_bb)
            self.call_if_not_empty(self.ts_2_om, self.om.handle_input_from_ts)
            self.call_if_not_empty(self.om_2_gw, self.ms.handle_order_from_gw)
            self.call_if_not_empty(self.gw_2_om, self.om.handle_input_from_market)
            self.call_if_not_empty(self.om_2_ts, self.ts.handle_response_from_om)


eb = EventBasedBackTester()


import yfinance as yf

import pandas as pd
#goog_data = yf.download(tickers='BTC-USD', start='2020-06-23', end='2021-08-12')
"""
goog_data = pd.read_csv("1.csv")
for line in zip(goog_data.index, goog_data['close']):
    date=line[0]
    price=line[1]
    price_information = {
        'date': date,
        'price': float(price)
    }
    eb.ts.rsi(price_information["price"])
    eb.ts.momentum(price_information["price"])
"""



#plt.plot(eb.ts.list_pnl)
#plt.plot(eb.ts.rsi_values)
#plt.show()

eb.process_data()
eb.process_events()


