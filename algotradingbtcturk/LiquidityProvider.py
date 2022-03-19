import time, base64, hmac, hashlib, requests, json
import pandas as pd
from OrderBook import OrderBook
from random import seed
from collections import deque
class LiquidityProvider:
    def __init__(self, lp_2_gateway):
        self.orders = []
        self.order_id = 0
        seed(0)
        self.lp_2_gateway = lp_2_gateway
        self.bestbidprice=0
        self.bestaskprice=0
        self.bestaskamount=0
        self.bestbidamount=0
    def read_tick_data_from_data_source(self):
        print(self.orders)
        pass

    def insert_manual_order(self, order):
        if self.lp_2_gateway is None:
            print('simulation mode')
            return order
        self.lp_2_gateway.append(order.copy())
