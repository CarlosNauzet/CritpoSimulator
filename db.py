import sqlite3
import os
from flask_wtf import FlaskForm
from wtforms import DateField, DecimalField, HiddenField, StringField, SubmitField



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
        # Tratar los datos
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

    def insert_query(self, query, data):
        conexion = sqlite3.connect(self.path) 
        cursor = conexion.cursor() 
        cursor.execute(query, data) # aquí execute está pillando query y reemplazada los valores en ? de VALUES para reemplazarlos por lo que hay guardado en la tupla de data
        conexion.commit()
        conexion.close()