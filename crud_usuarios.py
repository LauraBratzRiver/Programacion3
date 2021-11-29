import dbconexion

conexion = dbconexion.db_conexion()
class crud_usuarios:
    def consultar(self):
        return conexion.consultar("SELECT * FROM usuarios")

    def administrar_usuario(self, usuarios):
        if usuarios["accion"]=="nuevo":
            sql = "INSERT INTO usuarios (codigo, nombre, telefono) VALUES (%s, %s, %s)"
            val = (usuarios["codigo"], usuarios["nombre"], usuarios["telefono"])
        elif usuarios["accion"]=="modificar":
            sql = "UPDATE usuarios SET codigo=%s, nombre=%s, telefono=%s WHERE idUsuarios=%s"
            val = (usuarios["codigo"], usuarios["nombre"], usuarios["telefono"], usuarios["idUsuarios"])
        elif usuarios["accion"]=="eliminar":
            sql = "DELETE FROM usuarios WHERE idUsuarios=%s"
            val = (usuarios["idUsuarios"],)
        return conexion.ejecutar_consultas(sql, val)
    