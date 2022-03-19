from collections import deque

import numpy as np
import pandas as pd
import statistics as stats


def average(lst):
    return sum(lst) / len(lst)


class TradingStrategy:
    def __init__(self, ob_2_ts=None, ts_2_om=None, om_2_ts=None):
        self.orders = []
        self.order_id = 0
        self.i = 0
        self.a = 0
        self.yapilanloss = 0

        self.position = 0
        self.pnl = 0
        self.pnldiff = 0
        self.cash = 100
        self.paper_position = 0
        self.hold = False

        self.on_gun_icindeyapilanalis = 0
        self.current_offer = 0
        self.ob_2_ts = ob_2_ts
        self.ts_2_om = ts_2_om
        self.om_2_ts = om_2_ts
        self.long_signal = False
        self.oversold = False
        self.overbrought = False
        self.total = 0
        self.holdings = 0
        self.small_window = deque()
        self.large_window = deque()

        self.momentum_price = []
        self.ema_price = []

        self.btcquantity = 0

        self.paper_cash = 100000

        self.list_position = []
        self.list_cash = []
        self.list_holdings = []
        self.list_total = 0
        self.list_pnl = []

        self.avg_loss = 0
        self.avg_gain = 0


        self.last_price = 0
        self.difference_gain_history = []
        self.difference_loss_history = []
        self.avg_gain_values = []
        self.avg_loss_values = []
        self.rsi_values = []
        self.rsisayimi = 0
        self.gain_list = []
        self.loss_list = []

        self.avg_short_loss = 0
        self.avg_short_gain = 0

        self.avg_gain_values = []
        self.avg_loss_values = []

    def handle_input_from_bb(self, book_event=None):
        if self.ob_2_ts is None:
            print("simulation mode")
            self.handle_book_event(book_event)
        else:
            if len(self.ob_2_ts) > 0:
                be = self.handle_book_event(self.ob_2_ts.popleft())
                self.handle_book_event(be)

    def handle_book_event(self, book_event):
        if book_event is not None:
            self.current_bid = book_event['bid_price']
            self.current_offer = book_event['offer_price']
            self.signal(book_event)
            self.execution()

    def signal(self, book_event):

        if book_event['bid_quantity'] != -1 and book_event['offer_quantity'] != -1:

            self.create_metrics_with_prices(book_event['bid_price'])
            #self.rsi(book_event['bid_price'])
            self.buy_sell_or_hold(book_event)
    def ema(self, price):
        import  talib as ta
        self.ema_price.append(price)
        ema_price_list = np.array(self.ema_price)
        smalema = ta.EMA(ema_price_list,5)
        largeema = ta.EMA(ema_price_list,12)
        if smalema[-1] > largeema[-1]:
            return True
        else:
            return False
    def momentum(self, price):
        import talib as ta
        self.momentum_price.append(price)
        momentum_price_list = np.array(self.momentum_price)
        if self.a > 25:
            macd, macdsignal, macdhist = ta.MACD(momentum_price_list, fastperiod=12, slowperiod=26, signalperiod=9)
            print("macd degeri ", macdhist[-1])
            if macdsignal[-1] > macd[-1]:
                return True
            else:
                return False
        self.a+=1


    def rsi(self, price):
        self.rsisayimi+=1
        print(self.rsisayimi)
        """       import talib as ta
        self.rsi_index.append(price)
        rsi = ta.RSI(self.rsi_index, timeperiod=14)
        """

        if self.last_price == 0:
            self.last_price = price
        difference = price - self.last_price
        if difference != 0:
            if difference > 0:
                self.gain_list.append(difference)
            else:
                self.gain_list.append(0)
            if difference < 0:
                self.loss_list.append(-difference)
            else:
                self.loss_list.append(0)
            """short_gain_list = self.gain_list
            short_loss_list = self.loss_list
            if len(short_gain_list) > 14:
                del (short_loss_list[0])
                del (short_gain_list[0])
            
            if len(short_gain_list) > 0:
                self.avg_short_loss = stats.mean(short_loss_list)
                self.avg_short_gain = stats.mean(short_gain_list)
            short_rs = 0
            if self.avg_short_loss > 0:
                short_rs =self.avg_short_gain / self.avg_short_loss
            short_Rsi = 100 - (100 / (1 + short_rs))
            print(short_Rsi)
            if short_Rsi > 100:
                self.overbrought = True
                return 3
            """
            if len(self.gain_list) > 21:
                del (self.gain_list[0])
                del (self.loss_list[0])
            if len(self.gain_list) > 0:
                self.avg_gain = stats.mean(self.gain_list)
            if len(self.loss_list) > 0:
                self.avg_loss = stats.mean(self.loss_list)

            rs = 0
            if self.avg_loss > 0:
                rs = self.avg_gain / self.avg_loss
            self.last_price = price
            rsi = 100 - (100 / (1 + rs))
            print("rsi =", rsi)
            self.rsi_values.append(rsi)


            if rsi > 50:
                """
                self.on_gun_icindeyapilanalis = 0
                self.long_signal = True
                self.hold = False
                print("sinyal bulundu")
                """
                return True

            elif rsi < 50:
                """self.on_gun_icindeyapilanalis = 0
                self.long_signal = False
                self.hold = False
                print("satış")"""
                return False

                """self.on_gun_icindeyapilanalis += 1
                    self.long_signal = False
                    self.hold = True"""



    def create_metrics_with_prices(self, price_update):
        self.small_window.append(price_update)
        self.large_window.append(price_update)
        print(self.small_window)

        if len(self.small_window) > 5:
            self.small_window.popleft()
        if len(self.large_window) > 12:
            self.large_window.popleft()
        rsi = self.rsi(price_update)
        momentum = self.momentum(price_update)
        ema = self.ema(price_update)
        if len(self.small_window) == 5 and len(self.large_window) == 12:
            """if rsi == 3:
                self.overbrought = True
                self.hold = True
                self.long_signal = True
                return True"""
            if (ema and rsi) and (self.on_gun_icindeyapilanalis == 0):
                self.on_gun_icindeyapilanalis = 50
                self.long_signal = True
                self.hold = False
                print("sinyal bulundu")
                return True

            elif not ema and not rsi:
                self.on_gun_icindeyapilanalis = 0
                self.long_signal = False
                self.hold = False
                print("satış")
                return True
            else:
                self.on_gun_icindeyapilanalis -= 1
                if self.on_gun_icindeyapilanalis < 0:
                    self.on_gun_icindeyapilanalis = 0
                self.long_signal = False
                self.hold = True
                return True
        return False


    def buy_sell_or_hold(self, book_event):
        """if self.overbrought and self.cash > 5000:
            self.create_order(book_event, 5 * book_event['bid_quantity'], 'buy')
            self.position += 5 * book_event['bid_quantity'] / book_event['bid_price']
            self.holdings += 5 * book_event['bid_quantity']
            self.cash -= 5 * book_event['bid_quantity']
            self.i += 1
            self.overbrought = False"""




        if self.holdings < 15 and (self.pnldiff < -1.2 or self.pnldiff > 3.0) :
                print("loss emri 1")
                self.create_order(book_event, self.holdings, 'sell')
                self.cash -= -self.holdings
                self.holdings = 0
                self.position = 0
                self.i += 1
                self.yapilanloss+=1




        elif self.holdings < 25 and (self.pnldiff < -2.5 or self.pnldiff > 5.0) :#and not self.long_signal:
                print("loss emri 2 ")
                self.create_order(book_event, self.holdings, 'sell')
                self.cash -= -self.holdings
                self.holdings = 0
                self.position = 0
                self.i += 1

        elif self.holdings < 45 and (self.pnldiff < -5 or self.pnldiff > 9) : #and not self.long_signal:
                print("loss emri 3 ")
                self.create_order(book_event, self.holdings, 'sell')
                self.cash -= -self.holdings
                self.holdings = 0
                self.position = 0
                self.i += 1
        elif self.holdings < 80 and (self.pnldiff < -8 or self.pnldiff > 10):# and not self.long_signal:
                print("loss emri 4 ")
                self.create_order(book_event, self.holdings, 'sell')
                self.cash -= -self.holdings
                self.holdings = 0
                self.position = 0
                self.i += 1
        elif self.holdings < 100 and (self.pnldiff < -12 or self.pnldiff > 18): #and not self.long_signal:
                print("loss emri 4 ")
                self.create_order(book_event, self.holdings, 'sell')
                self.cash -= -self.holdings
                self.holdings = 0
                self.position = 0
                self.i += 1
        elif self.holdings < 200 and (self.pnldiff < -25 or self.pnldiff > 28): #and not self.long_signal:
                print("loss emri 4 ")
                self.create_order(book_event, self.holdings, 'sell')
                self.cash -= -self.holdings
                self.holdings = 0
                self.position = 0
                self.i += 1
        elif self.holdings < 400 and (self.pnldiff < -35 or self.pnldiff > 35) : #and not self.long_signal:
            print("loss emri 4 ")
            self.create_order(book_event, self.holdings, 'sell')
            self.cash -= -self.holdings
            self.holdings = 0
            self.position = 0
            self.i += 1
        elif self.holdings < 500 and (self.pnldiff < -50 or self.pnldiff > 60):
            print("loss emri 4 ")
            self.create_order(book_event, self.holdings, 'sell')
            self.cash -= -self.holdings
            self.holdings = 0
            self.position = 0
            self.i += 1
        elif self.holdings < 700 and (self.pnldiff < -60 or self.pnldiff > 70):
            print("loss emri 4 ")
            self.create_order(book_event, self.holdings, 'sell')
            self.cash -= -self.holdings
            self.holdings = 0
            self.position = 0
            self.i += 1







            # bid qunatityden satmıyoru bura yanlış oldu
        if self.long_signal and self.cash >= 20:
                self.create_order(book_event, book_event['bid_quantity'], 'buy')
                self.position += book_event['bid_quantity'] / book_event['bid_price']
                self.holdings += book_event['bid_quantity']
                self.cash -= book_event['bid_quantity']
                self.i += 1

        elif self.holdings > 0 and not self.long_signal and not self.hold:
            self.create_order(book_event, self.holdings, 'sell')
            self.cash -= -self.holdings
            self.holdings = 0
            self.position = 0
            self.i += 1
        self.holdings = self.position * book_event['bid_price']
        self.total = self.holdings + self.cash
        self.pnl = self.total - 100
        self.list_pnl.append(self.pnl)
        for i in range(len(self.list_pnl)):
            try:
                self.pnldiff = self.list_pnl[i] - self.list_pnl[i - 1]
            except:
                print("first time")
        print('total=%d, holding=%d, cash=%d, yapılantrade=%d pnl=%d pnldiff=%d' %
                (self.total, self.holdings, self.cash, self.i, self.pnl, self.pnldiff))

        self.list_position.append(self.list_total)
        self.list_cash.append(self.paper_cash)

    def create_order(self, book_event, quantity, side):
        self.order_id += 1

        ord = {
            'id': self.order_id,
            'price': book_event['bid_price'],
            'quantity': quantity,
            'side': side,
            'action': 'to_be_sent'
        }
        self.orders.append(ord.copy())


    def execution(self):
        orders_to_be_removed = []
        for index, order in enumerate(self.orders):
            if order['action'] == 'to_be_sent':
                print("emir gönderiliyor")
                order['status'] = 'new'
                order['action'] = 'no_action'
                if self.ts_2_om is None:
                    print("simulation mode")
                else:
                    self.ts_2_om.append(order.copy())
            if order['status'] == 'rejected' or order['status'] == 'cancelled':
                orders_to_be_removed.append(index)
            if order['status'] == 'filled':
                orders_to_be_removed.append(index)
                pos = order['quantity'] if order['side'] == 'buy' else -order['quantity']
                self.position += pos
                self.holdings = self.position * order['price']
                self.pnl -= pos * order['price']
                self.cash -= pos * order['price']
            for order_index in sorted(orders_to_be_removed, reverse=True):
                del (self.orders[order_index])

    def handle_response_from_om(self):
        if self.om_2_ts is not None:
            self.handle_market_response(self.om_2_ts.popleft())
        else:
            print("simulation mode")

    def handle_market_response(self, order_execution):
        print(order_execution)
        order, _ = self.lookup_orders(order_execution['id'])
        if order is None:
            print("errrooor !! not found")
        order['status'] = order_execution['status']
        self.execution()

    def lookup_orders(self, id):
        count = 0
        for o in self.orders:
            if o['id'] == id:
                return o, count
            count += 1

    def get_pnl(self):
        return self.pnl + self.position * (self.current_bid + self.current_offer) / 2
