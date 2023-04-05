import requests

API_KEY = "F8DD52B3-53AC-4AE0-818B-E2C62A964EE3"


class Purchase:

    def calculate(self, currency_origin, currency_dest, currency_origin_qty):
        coin_api = CoinApi()
        exchange_rate = coin_api.get_exchange_rate(
            origin=currency_origin,
            dest=currency_dest
        )
        return currency_origin_qty * exchange_rate['rate']


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
