from datetime import datetime
class Transactions:

    def get_all(self):
        return [
            {
            'id':1,
            'datetime': datetime.now(),
            'origin':'EUR',
            'dest':'BTC',
            'origin_qty':'1000',
            'dest_qty':'1',
            'pu':'1000'
            },
            {
            'id':2,
            'datetime': datetime.now(),
            'origin':'EUR',
            'dest':'BTC',
            'origin_qty':'1000',
            'dest_qty':'1',
            'pu':'1000'
            },
            {
            'id':3,
            'datetime': datetime.now(),
            'origin':'EUR',
            'dest':'BTC',
            'origin_qty':'1000',
            'dest_qty':'1',
            'pu':'1000'
            }
        ]