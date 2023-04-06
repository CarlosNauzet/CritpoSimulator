import requests

API_KEY = "F8DD52B3-53AC-4AE0-818B-E2C62A964EE3"


class Purchase:

    def __init__(
        self,
        currency_origin,
        currency_dest,
        currency_origin_qty,
        currency_dest_qty=0,
        date='',
        time=''
    ) -> None:
        self.currency_origin = currency_origin
        self.currency_dest = currency_dest
        self.currency_origin_qty = currency_origin_qty
        self.currency_dest_qty = currency_dest_qty
        self.date = date
        self.time = time
        # Add timestamp attribute

    def calculate(self):
        coin_api = CoinApi()
        exchange = coin_api.get_exchange_rate(
            origin=self.currency_origin,
            dest=self.currency_dest
        )
        self.currency_dest_qty = self.currency_origin_qty * exchange['rate']

    def get_price_unit(self):
        return self.currency_origin_qty / self.currency_dest_qty

    def save(self):
        ...


class CoinApi:

    def __init__(self):
        self.cambio = 0.0
        self.api_url = 'https://rest.coinapi.io'
        self.endpoint = '/v1/exchangerate'

    def get_exchange_rate(self, origin, dest):
        url = f'{self.api_url}{self.endpoint}/{origin}/{dest}'
        params = {
            'apiKey': API_KEY
        }
        response = requests.get(url, params=params)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(
                f'Error {response.status_code} {response.reason} al consultar la API'
            )
