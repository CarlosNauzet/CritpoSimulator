import datetime
import requests
from db import DBManager


API_KEY = "F8DD52B3-53AC-4AE0-818B-E2C62A964EE3"


class CalculatePurchase:

    def __init__(
        self,
        currency_origin,
        currency_dest,
        currency_origin_qty,
    ) -> None:
        self.currency_origin = currency_origin
        self.currency_dest = currency_dest
        self.currency_origin_qty = currency_origin_qty
        self.currency_dest_qty = 0

    def calculate(self):
        coin_api = CoinApi()
        exchange = coin_api.get_exchange_rate(
            origin=self.currency_origin,
            dest=self.currency_dest
        )
        self.currency_dest_qty = self.currency_origin_qty * exchange['rate']

    def get_price_unit(self):
        return self.currency_origin_qty / self.currency_dest_qty


class Purchase:
    def __init__(
        self,
        currency_origin,
        currency_dest,
        currency_origin_qty,
        currency_dest_qty,
        price_unit
    ) -> None:
        self.currency_origin = currency_origin
        self.currency_dest = currency_dest
        self.currency_origin_qty = currency_origin_qty
        self.currency_dest_qty = currency_dest_qty
        self.price_unit = price_unit

    def save(self):
        now = datetime.datetime.now()
        self.date = now.strftime('%d/%m/%Y')
        self.time = now.strftime('%H:%M:%S')

        query = """
            INSERT INTO transactions (date, time, _from, from_qty, _to, qty, pu) 
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        data = (
            self.date,
            self.time,
            self.currency_origin,
            self.currency_origin_qty,
            self.currency_dest,
            self.currency_dest_qty,
            self.price_unit
        )

        db_manager = DBManager()
        db_manager.insert_query(query, data)


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


class Transactions:

    def get_all(self):
        db_manager = DBManager()
        transactions = db_manager.querySQL(
            'SELECT id, date, time, _from, qty, _to, from_qty, pu FROM transactions'
        )
        return transactions

    def get_transacions_from_with_origin_currency(self, currency):
        db_manager = DBManager()
        return db_manager.querySQL(
            f"""
            
            SELECT  _from, qty, _to, from_qty FROM transactions WHERE _from = "{currency}" 
            
            """
        )

    def get_transacions_from_with_dest_currency(self, currency):
        db_manager = DBManager()
        return db_manager.querySQL(
            f"""
            
            SELECT  _from, qty, _to, from_qty FROM transactions WHERE _to = "{currency}" 
            
            """
        )


class Status:

    def get(self):
        total_eur = self.get_currency_status('EUR')
        all_currency = ['BTC','ETHC']

        for currency in all_currency:
            status = self.get_currency_status(currency)
            total = 0


        return total_eur - total

    def get_currency_status(currency):

        transactions = Transactions()
        transactions_origin = transactions.get_transacions_from_with_origin_currency(
            currency
        )
        transactions_dest = transactions.get_transacions_from_with_dest_currency(
            currency
        )

        total_to_qty = sum([
            transaction['qty']
            for transaction in transactions_origin
        ])

        total_from_qty = sum([
            transaction['from_qty']
            for transaction in transactions_dest
        ])

        return total_to_qty - total_from_qty

    # purchase tiene los dadtos guardados desde controller purchase
