class OrderBook:
    def __init__(self, gt_2_ob=None, ob_2_ts=None):
         self.list_asks = []
         self.list_bids = []
         self.gw_2_ob = gt_2_ob
         self.ob_2_ts = ob_2_ts
         self.current_bid = None
         self.current_ask = None
        


    def handle_order_from_gateway(self, order=None):
        if self.gw_2_ob is None:
            print("simulation mode")
            self.handle_new(order)
        elif len(self.gw_2_ob) > 0:
            order_from_gw = self.gw_2_ob.popleft()
            self.handle_order(order_from_gw)

    def handle_order(self, o):
        if o["action"] == 'new':
            self.handle_new(o)


        elif o['action'] == 'delete':
            self.handle_delete(o)

        return self.check_generate_top_of_book_event()
    def handle_new(self, o):
        if o['side'] == 'bid':
            self.list_bids.append(o)
            self.list_bids.sort(key=lambda x: x['price'], reverse=True)
        elif o['side'] == 'ask':
            self.list_asks.append(o)
            self.list_asks.sort(key=lambda x: x['price'])
    def get_list(self, o):
        if 'side' in o:
            if o['side'] == 'bid':
                lookup_list = self.list_bids
            elif o['side'] == 'ask':
                lookup_list = self.list_asks
            else:
                print("incorrect side")
                return None
            return lookup_list
        else:
            for order in self.list_bids:
                if order['id'] == o['id']:
                    return self.list_bids
            for order in self.list_asks:
                if order['id'] == o['id']:
                    return self.list_asks
            return None

    def find_order_in_a_list(self, o, lookup_list = None):
        if lookup_list is None:
            lookup_list = self.get_list(o)
        if lookup_list is not None:
            for order in lookup_list:
                if order['id'] == o['id']:
                    return order
            print("order not found1212")
        return None

    def handle_delete(self, o):
        lookup_list = self.get_list(o)
        order = self.find_order_in_a_list(o, lookup_list)
        if order is not None:
            lookup_list.remove(order)
        return None


    def check_generate_top_of_book_event(self):
        tob_changed= False

        current_list = self.list_bids
        if len(current_list)==0:
            if self.current_bid is not None:
                tob_changed =True
                self.current_bid = None
        else:
            if self.current_bid!=current_list[0]:

                tob_changed = True
                self.current_bid=current_list[0]
        current_list = self.list_asks
        if len(current_list) == 0:
            if self.current_ask is not None:
                tob_changed = True
                self.current_ask = None
        else:
            if self.current_ask != current_list[0]:
                tob_changed = True
                self.current_ask = current_list[0]

        if tob_changed:
            be=self.create_book_event(self.current_bid,
                                      self.current_ask)

            if self.ob_2_ts is not None:
                self.ob_2_ts.append(be)
            else:
                return be

    def create_book_event(self, bid, offer):
        book_event = {
                "bid_price": float(bid['price']) if bid else -1,
                "bid_quantity": float(bid['quantity']) if bid else -1,
                "offer_price": float(offer['price']) if offer else -1,
                "offer_quantity": float(offer['quantity']) if offer else -1
            }
        return book_event
    def crbosfonk(self, offer):
        
