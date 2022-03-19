class OrderManager:
    def __init__(self, ts_2_om = None, om_2_ts = None,
                 om_2_gw=None, gw_2_om=None):
        self.orders = []
        self.order_id = 0
        self.ts_2_om = ts_2_om
        self.om_2_ts = om_2_ts
        self.gw_2_om = gw_2_om
        self.om_2_gw = om_2_gw

    def handle_input_from_ts(self):
        if self.ts_2_om is not None:
            if len(self.ts_2_om)>0:
                self.handle_order_from_trading_strategy(self.ts_2_om.popleft())
        else:
            print("simulation mode")

    def handle_order_from_trading_strategy(self, order):
        order = self.create_new_order(order).copy()
        self.orders.append(order)
        if self.om_2_gw is None:
            print("simulation mode")
        else:
            self.om_2_gw.append(order.copy())
            print(self.om_2_gw)

    def create_new_order(self, order):

        if order['side'] == 'buy':
            neworder = {
                    'quantity': 20,
                    'price' : order['price'],
                    "newOrderClientId": "BtcTurk Python API Test",
                    'stopPrice' : 0,
                    "orderMethod": "market",
                    'orderType': order['side'],
                    "pairSymbol": "BTC_USDT"

                }
            return neworder
        elif order['side'] == 'sell':
            neworder = {
                'quantity': order['quantity'],
                'price': order['price'],
                "newOrderClientId": "BtcTurk Python API Test",
                'stopPrice': 0,
                "orderMethod": "market",
                'orderType': order['side'],
                "pairSymbol": "BTC_USDT"

            }


            return neworder
    def lookup_order_by_id(self, id):
        for i in range(len(self.orders)):
            if self.orders[i]['id'] == id:
                return self.orders[i]
        return None

    def clean_traded_orders(self):
        order_offsets = []
        for k in range(len(self.orders)):
            if self.orders[k]['status'] == 'filled':
                order_offsets.append(k)

        if len(order_offsets):
            for k in sorted(order_offsets, reverse=True):
                del (self.orders[k])

    def handle_input_from_market(self):
        if self.gw_2_om is not None:
            if len(self.gw_2_om)>0:
                self.handle_order_from_gateway(self.gw_2_om.popleft())
            else:
                print("simulation mode")
            self.clean_traded_orders()

    def handle_order_from_gateway(self, order_update):
        order = self.lookup_order_by_id(order_update['id'])
        if order is not None:
            order['status'] = order_update['status']
            if self.om_2_ts is not None:
                self.om_2_ts.append(order.copy())
            else:
                print("simulation mode")
            self.clean_traded_orders()
        else:
            print("order not found")