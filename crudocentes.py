import dbconexion

conexion = dbconexion.db_conexion()
class crud_docentes:
    def consultar(self):
        return conexion.consultar("""
            SELECT docentes.idDocente, docentes.codigo, docentes.nombre, docentes.telefono,
                docentes.idEscalafon, escalafon.escalafon
            FROM docentes
                INNER JOIN escalafon ON (escalafon.idEscalafon=docentes.idEscalafon)
        """)

    def administrar_docentes(self, docente):
        if docente["accion"]=="nuevo":
            sql = "INSERT INTO docentes (codigo, nombre, telefono, idEscalafon) VALUES (%s, %s, %s, %s)"
            val = (docente["codigo"], docente["nombre"], docente["telefono"], docente["idEscalafon"])
        elif docente["accion"]=="modificar":
            sql = "UPDATE docentes SET codigo=%s, nombre=%s, telefono=%s, idEscalafon=%s WHERE idDocente=%s"
            val = (docente["codigo"], docente["nombre"], docente["telefono"], docente["idEscalafon"], docente["idDocente"])
        elif docente["accion"]=="eliminar":
            sql = "DELETE FROM docentes WHERE idDocente=%s"
            val = (docente["idDocente"],)
        return conexion.ejecutar_consultas(sql, val)