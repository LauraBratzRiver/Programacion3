import dbconexion

conexion = dbconexion.db_conexion()
class crud_alumnos:
    def consultar(self):
        return conexion.consultar("SELECT * FROM alumnos")

    def administrar_alumno(self, alumno):
        if alumno["accion"]=="nuevo":
            sql = "INSERT INTO alumnos (codigo, nombre, telefono) VALUES (%s, %s, %s)"
            val = (alumno["codigo"], alumno["nombre"], alumno["telefono"])
        elif alumno["accion"]=="modificar":
            sql = "UPDATE alumnos SET codigo=%s, nombre=%s, telefono=%s WHERE idAlumno=%s"
            val = (alumno["codigo"], alumno["nombre"], alumno["telefono"], alumno["idAlumno"])
        elif alumno["accion"]=="eliminar":
            sql = "DELETE FROM alumnos WHERE idAlumno=%s"
            val = (alumno["idAlumno"],)
        return conexion.ejecutar_consultas(sql, val)
    