from base_datos import Base_Datos
from usuarios import Usuario_Cliente, Usuario_Admin
from validaciones import Validaciones

class GestorUsuarios:
    def __init__(self, base_datos):
        self.__bd = base_datos
        self.__bd.crear_tablas()
        
    # Registrar Clientes
    def crear_cliente(self, nombre, email, ciudad):
        Usuario_Cliente(0, nombre, email, ciudad)

        ciudad = Validaciones.sanear_ciudad(ciudad)

        sql = """
            INSERT INTO usuarios
            (tipo, nombre, email, ciudad_frecuente)
            VALUES (?, ?, ?, ?)
        """
        resultado = self.__bd.ejecutar(
            sql, ("cliente", nombre.strip(), email.strip(), ciudad)
        )
        if resultado is None:
            return None
        return resultado[0]

    # Registrar Administrador
    def crear_admin(self, nombre, email, nivel):
        Usuario_Admin(0, nombre, email, nivel)
        sql = """
            INSERT INTO usuarios
            (tipo, nombre, email, nivel_acceso)
            VALUES (?, ?, ?, ?)
        """
        resultado = self.__bd.ejecutar(
            sql, ("admin", nombre.strip(), email.strip(), nivel)
        )
        if resultado is None:
            return None

        return resultado[0]

    # Listar Usuarios
    def listar(self):
        return self.__bd.consultar(
            "SELECT * FROM ORDER BY id"
        )

    # Buscar Usuario
    def buscvar_por_id(self, id_usuario):
        filas = self.__bd.consultar(
            "SELECT * FROM usuarios WHERE ID = ?", 
            (id_usuario,)
        )

        if filas:
            return filas[0]

        return None

    # Modificar Nombre
    def actualizar_nombre(self, id_usuario, nombre):
        if not Validaciones.validar_texto_no_vacio(nombre):
            resultado = self.__bd.ejecutar(
                "UPDATE usuarios SET nombre = ? WHERE id = ?",
                (nombre.strip(), id_usuario)
            )

            return resultado is not None and resultado[1] > 0

    # Eliminar Usuario
    def eliminar(self, id_usuario):
        resultado = self.__bd.ejecutar(
            "DELETE FROM usuarios WHERE id  = ?",
            (id_usuario,)
        )

        return resultado is not None and resultado[1] > 0