import sqlite3
from datetime import datetime

"""
SELECT id, date, time, _from, qty, _to, from_qty, pu FROM transactions
"""


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
    
class DBManager:
    def __init__(self, ruta):
         self.ruta = ruta

    def consultaSQL(self, consulta):


        # Conectar a la base de datos
        conexion = sqlite3.connect(self.ruta)
        # Crear un cursor
        cursor = conexion.cursor()
        # Ejecutar la consulta SQL sobre ese cursor
        cursor.execute(consulta)
        cursor.fetchall        # Tratar los datos
        #obtener los datos
        datos = cursor.fetchall()

        
         # name_columns = ['id', 'date', 'time', '_from', 'qty', '_to', 'from_qty', 'pu']
        
        """MANERA MANUAL DE HACERLO
        for dato in datos:
            realtransaction = {
                'id': dato[0],
                'date': dato[1],
                'time': dato[2],
                '_from': dato[3],
                'qty': dato[4],
                '_to': dato[5],
                'from_qty': dato[6],
                'pu': dato[7]
            }
            self.realtransactions.append(realtransaction)
            """
            
        self.realtransactions = []
        name_columns = []
        for column in cursor.description:
            name_columns.append(column[0])

        for dato in datos:
            indice = 0
            realtransaction = {}
            for name in name_columns:
                realtransaction[name] = dato[indice]
                indice += 1

            self.realtransactions.append(realtransaction)

         # cerrar la conexión
        conexion.close()
            

        return self.realtransactions





    
         