import datetime
import requests
from db import DBManager


API_KEY ="54CC9DB5-A9E5-4DEF-AFCA-BFAEE77C7995"  #"F8DD52B3-53AC-4AE0-818B-E2C62A964EE3"


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
        data = ( #
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

    def get_transacions_with_from_currency(self, currency):
        db_manager = DBManager()
        return db_manager.querySQL(
            f"""
            
            SELECT  _from, qty, _to, from_qty FROM transactions WHERE _from = "{currency}" 
            
            """
        )

    def get_transacions_with_to_currency(self, currency):
        db_manager = DBManager()
        return db_manager.querySQL(
            f"""
            
            SELECT  _from, qty, _to, from_qty FROM transactions WHERE _to = "{currency}" 
            
            """
        )

    def get_currency_balance(self, currency):
        transactions_from = self.get_transacions_with_from_currency(
            currency
        )

        transactions_to = self.get_transacions_with_to_currency(
            currency
        )

        total_from_qty = sum([
            transaction['from_qty']
            for transaction in transactions_from
        ])

        total_to_qty = sum([
            transaction['qty']
            for transaction in transactions_to
        ])

        return total_to_qty - total_from_qty

    def get_initial_euros_investment(self):
        transactions_from = self.get_transacions_with_from_currency(
            'EUR'
        )

        total_from_qty = sum([
            transaction['from_qty']
            for transaction in transactions_from
        ])

        return total_from_qty


class Status:

    def get_balance_by_currency(self):

        transactions = Transactions()

        all_currencies = [
            'EUR',
            'BTC',
            'ETH',
            'USDT',
            'ADA',
            'SOL',
            'XRP',
            'DOT',
            'DOGE',
            'SHIB'
        ]

        balance_by_currency = {}

        for currency in all_currencies:
            balance = transactions.get_currency_balance(currency)
            if balance > 0:
                balance_by_currency[currency] = balance

        return balance_by_currency

    def get_current_euro_invesment_amount(self, balance_by_currency):
        coin_api = CoinApi()
        total_euros_investment = 0

        for currency, balance in balance_by_currency.items():
            exchange = coin_api.get_exchange_rate(currency, 'EUR')
            euros_amount = exchange['rate'] * balance
            # es una abreviacion de total = total + euros (total+=euros)
            total_euros_investment += euros_amount

        return total_euros_investment
