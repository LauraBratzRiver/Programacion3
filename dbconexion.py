import mysql.connector

class db_conexion:
    def __init__(self):
        print("Iniciando conexion con la base de datos...")
        self.db = mysql.connector.connect(
            host="localhost",
            port=3306,
            user="root",
            passwd="",
            database="db_agroHelping"
        )
        if self.db.is_connected():
            print("Conexion establecida")
        else:
            print("Conexion fallida")

    def consultar(self, sql):
        cursor = self.db.cursor(dictionary=True)
        cursor.execute(sql)
        result = cursor.fetchall()
        return result

    def ejecutar_consultas(self, sql, val):
        try:
            cursor = self.db.cursor()
            cursor.execute(sql, val)
            self.db.commit()
            return "Registro procesado con exito"
        except Exception as e:
            return "Error: " + str(e)