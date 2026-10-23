from datetime import date
from base_datos import Base_Datos
from validaciones import Validaciones

class GestorEmpleados:
    def __init__(self, base_datos):
        self.__bd = base_datos
        self.__bd.crear_tabla_empleados()

    #Registrar Empleado
    def registrar_empleado(self, id_empleados, nombre, direccion, telefono, correo, fecha_inicio, salario):
        if type(id_empleados) is not int or id_empleados <= 0:
            return False
        
        if not isinstance(nombre, str):
            return False

        if not Validaciones.validar_texto_no_vacio(nombre):
            return False

        if not isinstance(correo, str):
            return False

        if not Validaciones.validar_email(correo):
            return False

        if not isinstance(fecha_inicio, date):
            return False

        if (isinstance(salario, bool) or not isinstance(salario, (int, float)) or salario < 0):
            return False

        sql = """
            INSERT INTO Empleados (
            ID_Empleados, 
            Nombre, 
            Direccion, 
            Telefono,
            Correo,
            Fecha_Inicio,
            Salario)
            VALUES (?,?,?,?,?,?,?)
        """

        datos = (
            id_empleados,
            nombre.strip(),
            direccion,
            telefono,
            correo.strip(),
            fecha_inicio.isoformat(),
            salario
        )

        resultado = self.__bd.ejecutar(sql, datos)
        return resultado is not None and resultado[1] > 0

    #Listar Empleados
    def listar_empleados(self):
        return self.__bd.consultar(
            "SELECT * FROM empleados ORDER BY ID_Empleados"
        )

    #Buscar Empleados por ID
    def buscar_por_id(self, ID_Empleados):
        filas = self.__bd.consultar(
            "SELECT * FROM empleados WHERE ID_Empleados = ?",
            (ID_Empleados,)
        )

        if filas:
            return filas [0]
        return None

    #Actualizar Nombre
    def actualizar_nombre(self, ID_Empleados, nombre):
        if not isinstance(nombre, str):
            return False

        if not Validaciones.validar_texto_no_vacio(nombre):
            return False

        resultado = self.__bd.ejecutar(
            "UPDATE empleados SET Nombre = ? WHERE ID_Empleados = ?",
            (nombre.strip(), ID_Empleados)
        )

        return resultado is not None and resultado[1] > 0

    #Eliminar Empleado
    def eliminar_empleado(self, ID_Empleados):
        resultado = self.__bd.ejecutar(
            "DELETE FROM empleados WHERE ID_Empleados = ?",
            (ID_Empleados,)
        )

        return resultado is not None and resultado[1] > 0