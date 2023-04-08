from db import DBManager


class Transactions:

    def get_all(self):
        db_manager = DBManager()
        transactions = db_manager.querySQL(
            'SELECT id, date, time, _from, qty, _to, from_qty, pu FROM transactions'
        )
        return transactions
    
    #purchase tiene los dadtos guardados desde controller purchase
    
       