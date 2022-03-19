
class MarketSimulator:
    def __init__(self, om_2_gw=None, gw_2_om=None):
        self.orders = []
        self.om_2_gw = om_2_gw
        self.gw_2_om = gw_2_om


    def handle_order_from_gw(self):
        if self.om_2_gw is not None:
            if len(self.om_2_gw) > 0:
                self.handle_order(self.om_2_gw.popleft())

        else:
            print("simulation mode")

    def handle_order(self, order):
        import time, base64, hmac, hashlib, requests, json

        base = "https://api.btcturk.com"
        method = "/api/v1/order"
        uri = base + method

        apiKey = "1a58a0c9-9630-4d73-8294-7e8a9da8e3b1"
        apiSecret = "jvn9TlU45SGMm7ljl2KOGVpfY7yTwQdd"
        apiSecret = base64.b64decode(apiSecret)

        stamp = str(int(time.time()) * 1000)
        data = "{}{}".format(apiKey, stamp).encode("utf-8")
        signature = hmac.new(apiSecret, data, hashlib.sha256).digest()
        signature = base64.b64encode(signature)
        headers = {"X-PCK": apiKey, "X-Stamp": stamp, "X-Signature": signature, "Content-Type": "application/json"}


        result = requests.post(url=uri, headers=headers, json=order)
        result = result.json()
        print(json.dumps(result, indent=2))


