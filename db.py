import sqlite3
import os


class DBManager:
    def __init__(self):
        self.path = os.path.join('data', 'data_transactions.db')

    def querySQL(self, consulta):

        # Conectar a la base de datos
        conexion = sqlite3.connect(self.path)
        # Crear un cursor
        cursor = conexion.cursor()
        # Ejecutar la consulta SQL sobre ese cursor
        cursor.execute(consulta)
        cursor.fetchall        # Tratar los datos
        # obtener los datos
        rows = cursor.fetchall()

        self.realtransactions = []
        name_columns = []
        for column in cursor.description:
            name_columns.append(column[0])

        for row in rows:
            indice = 0
            realtransaction = {}
            for name in name_columns:
                realtransaction[name] = row[indice]
                indice += 1

            self.realtransactions.append(realtransaction)

         # cerrar la conexión
        
        return self.realtransactions

    def insert_query(self, query):
        conexion = sqlite3.connect(self.path) # creamos al BDD
        cursor = conexion.cursor() # genremos el cursor
        cursor.execute(query) # no es fetch, execute el query del INSERT id, date, etc... (buscar como se hace un insert)
        conexion.close()