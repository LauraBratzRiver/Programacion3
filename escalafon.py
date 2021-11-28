import dbconexion

conexion = dbconexion.db_conexion()
class escalafon:
    def consultar(self):
        return conexion.consultar("SELECT * FROM escalafon")